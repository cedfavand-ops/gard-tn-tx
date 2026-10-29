"""Descente d'échelle de Tn et Tx."""
from datetime import timedelta
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from . import config as C


def to_grid(lon, lat, v, grid):
    pts = np.column_stack([lon, lat])
    out = LinearNDInterpolator(pts, v)(grid.LON, grid.LAT)
    bad = ~np.isfinite(out)
    if bad.any():
        out[bad] = NearestNDInterpolator(pts, v)(grid.LON[bad], grid.LAT[bad])
    return out.astype(np.float32)


def window_stat(icon, D, window, fn):
    t0, t1 = D + timedelta(hours=window[0]), D + timedelta(hours=window[1])
    idx = [i for i, t in enumerate(icon.times) if t0 <= t <= t1]
    if not idx:
        raise RuntimeError("Aucune échéance du modèle dans la fenêtre demandée")
    truncated = icon.times[idx[-1]] < t1 - timedelta(hours=1)
    return fn(icon.t2m[idx], axis=0), icon.times[idx[-1]], truncated


def inversion_index(icon):
    if len(icon.night_times) == 0:
        return 0.0, float("nan"), float("nan")
    cloud, wind = float(np.mean(icon.cloud)), float(np.mean(icon.wind))
    fc = np.clip((C.CLOUD_ZERO - cloud) / (C.CLOUD_ZERO - C.CLOUD_FULL), 0, 1)
    fw = np.clip((C.WIND_ZERO - wind) / (C.WIND_ZERO - C.WIND_FULL), 0, 1)
    return float(fc * fw), wind, cloud


def compute(icon, dem, mask, hp, grid, D, force_inversion=None):
    zm = gaussian_filter(dem, C.ZM_SIGMA_M / grid.res)       # orographie « vue » par le modèle
    dz = dem - zm

    # --- Tn
    tn_pts, tn_end, tn_trunc = window_stat(icon, D, C.TN_WINDOW, np.min)
    tn_m = to_grid(icon.lon, icon.lat, tn_pts, grid)
    tn_plain = tn_m + C.LAPSE_TN * dz
    inv, wind, cloud = inversion_index(icon)
    if force_inversion is not None:
        inv = float(force_inversion)
    obs = np.isfinite(hp)
    w_obs = np.clip(gaussian_filter(obs.astype(np.float32), 4) * 1.2, 0, 1)   # fondu aux bords
    w = inv * w_obs
    tn_rad = tn_m + C.AMP_LST_TO_AIR * np.nan_to_num(hp)
    tn = (1 - w) * tn_plain + w * tn_rad

    # --- Tx (pas d'ECOSTRESS : valeurs du modèle corrigées du relief)
    tx_pts, tx_end, tx_trunc = window_stat(icon, D, C.TX_WINDOW, np.max)
    tx = to_grid(icon.lon, icon.lat, tx_pts, grid) + C.LAPSE_TX * dz

    tn[~mask] = np.nan
    tx[~mask] = np.nan
    info = dict(inversion=inv, wind=wind, cloud=cloud,
                tn_end=tn_end, tn_truncated=bool(tn_trunc),
                tx_end=tx_end, tx_truncated=bool(tx_trunc),
                ecostress_cover=float(np.mean(obs[mask])))
    return tn, tx, info
