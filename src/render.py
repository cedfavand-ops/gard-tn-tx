"""Rendu : PNG coloré + PNG de valeurs (pour lire la température au clic) + meta.json."""
import json
import numpy as np
from PIL import Image
from . import config as C
from .contours import isolines


def to_mercator(a, grid):
    """Rééchantillonne les lignes en projection Web Mercator pour L.imageOverlay."""
    lon0, lat0, lon1, lat1 = grid.bounds
    m = lambda la: np.log(np.tan(np.pi / 4 + np.radians(la) / 2))
    dx = np.radians(grid.dlon)
    h = int(round((m(lat1) - m(lat0)) / dx))
    ym = m(lat1) - (np.arange(h) + .5) * dx
    lat = np.degrees(2 * np.arctan(np.exp(ym)) - np.pi / 2)
    r = (lat1 - lat) / grid.dlat - 0.5
    r0 = np.clip(np.floor(r).astype(int), 0, grid.ny - 2)
    f = np.clip(r - r0, 0, 1)[:, None]
    return a[r0] * (1 - f) + a[r0 + 1] * f


def colorize(a, vmin, vmax):
    pos = np.array([s[0] for s in C.STOPS]); rgb = np.array([s[1] for s in C.STOPS], float)
    x = np.clip((a - vmin) / (vmax - vmin), 0, 1)
    out = np.zeros(a.shape + (4,), np.uint8)
    for c in range(3):
        out[..., c] = np.interp(np.nan_to_num(x), pos, rgb[:, c])
    out[..., 3] = np.where(np.isfinite(a), 255, 0)
    return out


def value_png(a):
    q = np.clip(np.round((np.nan_to_num(a, nan=-100) + 50) * 100), 0, 65535).astype(np.uint16)
    q[~np.isfinite(a)] = 0
    rgb = np.zeros(a.shape + (3,), np.uint8)
    rgb[..., 0], rgb[..., 1], rgb[..., 2] = q >> 8, q & 255, 255
    return rgb


def write_all(out, grid, tn, tx, mask, icon, info, D):
    scale = {}
    for name, a in (("tn", tn), ("tx", tx)):
        v = a[np.isfinite(a)]
        vmin, vmax = np.floor(np.percentile(v, 1)), np.ceil(np.percentile(v, 99))
        if vmax - vmin < 6:
            vmax = vmin + 6
        am = to_mercator(a, grid)
        Image.fromarray(colorize(am, vmin, vmax), "RGBA").save(f"{out}/{name}.png", optimize=True)
        Image.fromarray(value_png(am), "RGB").save(f"{out}/{name}_val.png", optimize=True)
        scale[name] = (float(vmin), float(vmax))
        print(f"[RENDU] {name}: {isolines(a, grid, f'{out}/{name}_iso.geojson')} isolignes", flush=True)
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    from datetime import timedelta
    meta = dict(
        generated=iso(__import__("datetime").datetime.now(__import__("datetime").timezone.utc)),
        run=iso(icon.run), demo=icon.demo, res=grid.res, bounds=list(grid.bounds),
        inversion=round(info["inversion"], 2),
        wind=None if np.isnan(info["wind"]) else round(info["wind"], 1),
        cloud=None if np.isnan(info["cloud"]) else round(info["cloud"]),
        ecostress=C.ECOSTRESS_LABEL, ecostress_cover=round(info["ecostress_cover"], 2),
        tn=dict(vmin=scale["tn"][0], vmax=scale["tn"][1],
                start=iso(D + timedelta(hours=C.TN_WINDOW[0])), end=iso(D + timedelta(hours=C.TN_WINDOW[1])), last=iso(info["tn_end"]),
                truncated=info["tn_truncated"]),
        tx=dict(vmin=scale["tx"][0], vmax=scale["tx"][1],
                start=iso(D + timedelta(hours=C.TX_WINDOW[0])), end=iso(D + timedelta(hours=C.TX_WINDOW[1])), last=iso(info["tx_end"]),
                truncated=info["tx_truncated"]),
        stops=[[p, list(c)] for p, c in C.STOPS],
    )
    with open(f"{out}/meta.json", "w") as f:
        json.dump(meta, f, indent=1)
