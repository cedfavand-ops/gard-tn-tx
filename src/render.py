"""Rendu : PNG coloré + PNG de valeurs (lecture au survol) + isolignes + meta.json."""
import json
from datetime import datetime, timedelta, timezone
import numpy as np
from PIL import Image
from . import config as C
from .contours import isolines

# réglages propres à chaque carte
SPECS = {
    "tn":   dict(label="Tn", unit="°C", dec=1, minw=0.1, band=lambda: C.BAND, iso=(1.0, 5.0), pal="temp"),
    "tx":   dict(label="Tx", unit="°C", dec=1, minw=0.1, band=lambda: C.BAND, iso=(1.0, 5.0), pal="temp"),
    "gust": dict(label="Rafale max", unit="km/h", dec=0, minw=1.0, band=lambda: C.BAND_GUST, iso=(5.0, 20.0), pal="gust"),
}


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


def class_scale(am, vmin, vmax, band, n_total, minw=0.1, dec=1):
    """Bornes des classes intermédiaires entre lo et hi : mélange pas régulier / effectifs égaux,
    largeur de classe bornée (minw ... CLASS_MAX_WIDTH_FACTOR x pas régulier)."""
    lo, hi = vmin + band, vmax - band
    n = int(min(n_total - 2, max(2, int(round((hi - lo) / minw)))))
    vals = am[np.isfinite(am)]
    lin = lo + (hi - lo) * np.arange(n + 1) / n
    f_lo, f_hi = (vals < lo).mean(), (vals < hi).mean()
    q = np.quantile(vals, f_lo + (f_hi - f_lo) * np.arange(n + 1) / n)
    t = (1 - C.CLASS_QUANTILE_MIX) * lin + C.CLASS_QUANTILE_MIX * q
    w = np.diff(t)
    wmax = C.CLASS_MAX_WIDTH_FACTOR * (hi - lo) / n
    for _ in range(50):                              # borne les largeurs puis renormalise
        w = np.clip(w, minw, wmax)
        w *= (hi - lo) / w.sum()
    t = np.round(lo + np.concatenate([[0.0], np.cumsum(w)]), dec)
    t[0], t[-1] = round(lo, dec), round(hi, dec)
    for k in range(1, n + 1):                        # largeur minimale après arrondi
        t[k] = max(t[k], t[k - 1] + minw)
    if t[-1] > hi + 1e-6:
        t = np.round(lin, dec)
    return t


def class_colors(n, pal="temp"):
    """extrême bas, n classes intermédiaires, extrême haut. Palette fixe si n == 18, sinon échantillonnée dessus."""
    low, mid, high = ((C.CLASS_PINK, C.CLASS_PALETTE, C.CLASS_RED) if pal == "temp"
                      else (C.GUST_LOW, C.GUST_PALETTE, C.GUST_HIGH))
    p = np.array(mid, float)
    if n != len(p):
        pos = np.linspace(0, 1, len(p))
        p = np.stack([np.interp((np.arange(n) + .5) / n, pos, p[:, c]) for c in range(3)], axis=1)
    return np.vstack([low, p, high]).round().astype(np.uint8)


def colorize_classes(a, t, colors):
    idx = np.digitize(np.nan_to_num(a, nan=t[0]), t)
    out = np.zeros(a.shape + (4,), np.uint8)
    out[..., :3] = colors[idx]
    out[..., 3] = np.where(np.isfinite(a), 255, 0)
    return out


def value_png(a):
    q = np.clip(np.round((np.nan_to_num(a, nan=-100) + 50) * 100), 0, 65535).astype(np.uint16)
    q[~np.isfinite(a)] = 0
    rgb = np.zeros(a.shape + (3,), np.uint8)
    rgb[..., 0], rgb[..., 1], rgb[..., 2] = q >> 8, q & 255, 255
    return rgb


def _render_field(out, name, a, grid):
    sp = SPECS[name]
    step = 10.0 ** (-sp["dec"])
    am = to_mercator(a, grid)
    vmin = np.floor(np.nanmin(am) / step) * step           # extrêmes réels de la carte
    vmax = np.ceil(np.nanmax(am) / step) * step
    band = min(sp["band"](), (vmax - vmin) / 4)
    lo, hi = vmin + band, vmax - band
    classes = None
    if C.N_CLASSES.get(name):
        t = class_scale(am, vmin, vmax, band, C.N_CLASSES[name], sp["minw"], sp["dec"])
        cols = class_colors(len(t) - 1, sp["pal"])
        edges = [vmin] + [float(x) for x in t] + [vmax]
        classes = [dict(a=edges[k], b=edges[k + 1], rgb=[int(x) for x in cols[k]]) for k in range(len(cols))]
        img = colorize_classes(am, t, cols)
        lo, hi = float(t[0]), float(t[-1])
    else:
        img = colorize(am, lo, hi)
    Image.fromarray(img, "RGBA").save(f"{out}/{name}.png", optimize=True)
    Image.fromarray(value_png(am), "RGB").save(f"{out}/{name}_val.png", optimize=True)
    n = isolines(a, grid, f"{out}/{name}_iso.geojson", minor=sp["iso"][0], major=sp["iso"][1])
    print(f"[RENDU] {name}: {n} isolignes", flush=True)
    return dict(label=sp["label"], unit=sp["unit"], dec=sp["dec"], vmin=float(vmin), vmax=float(vmax),
                lo=float(lo), hi=float(hi), classes=classes)


def write_all(out, grid, tn, tx, mask, icon, info, D, gust=None, gust_info=None):
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = dict(
        generated=iso(datetime.now(timezone.utc)),
        run=iso(icon.run), demo=icon.demo, res=grid.res, bounds=list(grid.bounds),
        inversion=round(info["inversion"], 2), inversion_lo=round(info["inversion_lo"], 2),
        inversion_hi=round(info["inversion_hi"], 2),
        wind=None if np.isnan(info["wind"]) else round(info["wind"], 1),
        cloud=None if np.isnan(info["cloud"]) else round(info["cloud"]),
        ecostress=C.ECOSTRESS_LABEL, ecostress_cover=round(info["ecostress_cover"], 2),
        stops=[[p, list(c)] for p, c in C.STOPS],
    )
    meta["tn"] = dict(_render_field(out, "tn", tn, grid),
                      start=iso(D + timedelta(hours=C.TN_WINDOW[0])), end=iso(D + timedelta(hours=C.TN_WINDOW[1])),
                      last=iso(info["tn_end"]), truncated=info["tn_truncated"])
    meta["tx"] = dict(_render_field(out, "tx", tx, grid),
                      start=iso(D + timedelta(hours=C.TX_WINDOW[0])), end=iso(D + timedelta(hours=C.TX_WINDOW[1])),
                      last=iso(info["tx_end"]), truncated=info["tx_truncated"])
    if gust is not None:
        g = gust_info
        meta["gust"] = dict(_render_field(out, "gust", gust, grid), start=iso(g["start"]), end=iso(g["end"]),
                            last=iso(g["last"]), truncated=g["truncated"], dir_deg=round(g["dir_deg"]),
                            dir_name=g["dir_name"], tz=C.GUST_TZ)
    with open(f"{out}/meta.json", "w") as f:
        json.dump(meta, f, indent=1)
