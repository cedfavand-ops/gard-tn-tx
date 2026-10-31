"""Rafales : exposition au vent (indice d'abri Sx par secteur) et descente d'échelle de VMAX_10M."""
import os
import numpy as np
from scipy.ndimage import gaussian_filter
from . import config as C
from .forecast import to_grid


def _take(a, ox, oy):
    p = max(abs(ox), abs(oy), 1)
    ap = np.pad(a, p, mode="edge")
    ny, nx = a.shape
    return ap[p + oy:p + oy + ny, p + ox:p + ox + nx]


def sx_stack(dem, grid):
    """Sx (degrés) pour 8 secteurs (vent venant de 0°, 45°, ...). Sx > 0 : relief plus haut en amont (abri),
    Sx < 0 : le terrain s'abaisse en amont (exposition). Mis en cache dans data/sx_<res>.npz."""
    path = f"data/sx_{grid.res}.npz"
    if os.path.exists(path):
        return np.load(path)["sx"].astype(np.float32)
    sx = np.zeros((8,) + dem.shape, np.float32)
    for i in range(8):
        phi = np.radians(45 * i)
        best = np.full(dem.shape, -90.0, np.float32)
        for d in C.SX_DISTANCES_M:
            ox = int(round(d * np.sin(phi) / grid.res))        # amont = direction d'où vient le vent
            oy = int(round(-d * np.cos(phi) / grid.res))       # lignes croissantes vers le sud
            ang = np.degrees(np.arctan((_take(dem, ox, oy) - dem) / d))
            best = np.maximum(best, ang)
        sx[i] = best
    os.makedirs("data", exist_ok=True)
    np.savez_compressed(path, sx=sx.astype(np.float16))
    return sx


def sx_at(sx, phi):
    x = (phi % 360.0) / 45.0
    f0 = np.floor(x)
    i0 = f0.astype(int) % 8
    i1 = (i0 + 1) % 8
    yy, xx = np.indices(phi.shape)
    return (1 - (x - f0)) * sx[i0, yy, xx] + (x - f0) * sx[i1, yy, xx]


def compass(deg):
    names = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"]
    return names[int(((deg % 360) + 11.25) // 22.5) % 16]


def compute_gust(icon, dem, mask, grid, D, sx):
    """Rafale max (km/h) sur le jour civil de demain, ramenée à la maille. Renvoie (champ, info, champs archivés)."""
    from .timewin import gust_window_utc
    s, e = gust_window_utc(D)
    g = icon.gust                                          # (nt, npts) m/s, NaN si échéance manquante
    ok = np.isfinite(g).any(axis=0)
    gz = np.where(np.isfinite(g), g, -1.0)
    kmax = gz.argmax(axis=0)
    gpts = gz.max(axis=0) * 3.6
    # direction du vent à l'heure de la rafale maximale (échéance U/V la plus proche)
    uv_t = np.array([(t - s).total_seconds() for t in icon.uv_times])
    idx = np.array([np.abs(uv_t - (icon.gust_times[k] - s).total_seconds()).argmin() for k in range(len(icon.gust_times))])
    cols = np.arange(g.shape[1])
    u_at, v_at = icon.u10[idx[kmax], cols], icon.v10[idx[kmax], cols]
    g_m = to_grid(icon.lon[ok], icon.lat[ok], gpts[ok], grid)
    u_g = to_grid(icon.lon, icon.lat, u_at, grid)
    v_g = to_grid(icon.lon, icon.lat, v_at, grid)
    phi = np.degrees(np.arctan2(-u_g, -v_g)) % 360.0       # direction d'où vient le vent
    zm = gaussian_filter(dem, C.ZM_SIGMA_M / grid.res)
    dz = dem - zm
    s_x = sx_at(sx, phi)
    fac = (1 + C.GUST_Z_GAIN * np.clip(dz / 100.0, -1, 1)
           + C.GUST_SX_GAIN * np.clip(-s_x / C.GUST_SX_SCALE_DEG, -1, 1))
    fac = np.clip(fac, *C.GUST_FACTOR_BOUNDS)
    fac = fac / gaussian_filter(fac, C.ZM_SIGMA_M / grid.res)   # conserve la moyenne à l'échelle du modèle
    gust = (g_m * fac).astype(np.float32)
    gust[~mask] = np.nan
    last = max(t for k, t in enumerate(icon.gust_times) if np.isfinite(g[k]).any())
    um, vm = float(np.nanmean(u_g[mask])), float(np.nanmean(v_g[mask]))
    dirdeg = float(np.degrees(np.arctan2(-um, -vm)) % 360.0)
    info = dict(start=s, end=e, last=last, truncated=bool(last < e - __import__("datetime").timedelta(hours=1)),
                dir_deg=dirdeg, dir_name=compass(dirdeg),
                factor_min=float(np.nanmin(fac[mask])), factor_max=float(np.nanmax(fac[mask])))
    return gust, info, dict(gust_model=g_m, gust_factor=fac)
