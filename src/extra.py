"""Pluie (cumul du jour civil de demain) et nuages (bas / moyens / élevés) sur la grille."""
import numpy as np
from .forecast import to_grid


def compute_rain(icon, mask, grid):
    r = np.clip(to_grid(icon.lon, icon.lat, icon.rain, grid), 0, None)
    r[~mask] = np.nan
    return r.astype(np.float32), icon.rain_meta


def compute_clouds(icon, mask, grid):
    out = {}
    for hh, c in icon.clouds.items():
        layers = []
        for k in ("low", "mid", "high"):
            a = np.clip(to_grid(icon.lon, icon.lat, c[k], grid), 0, 100)
            a[~mask] = np.nan
            layers.append(a.astype(np.float32))
        out[hh] = dict(time=c["time"], low=layers[0], mid=layers[1], high=layers[2])
    return out
