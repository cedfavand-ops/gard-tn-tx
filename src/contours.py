"""Isolignes GeoJSON : fines tous les 1 °C, épaisses (major) tous les 5 °C."""
import json
import numpy as np
from contourpy import contour_generator
from .static import norm_gauss


def isolines(a, grid, path, smooth_m=225.0, min_pts=8):
    s, _ = norm_gauss(a, smooth_m / grid.res)        # lissage tenant compte des NaN
    z = np.ma.masked_invalid(s[::-1])                 # latitudes croissantes
    gen = contour_generator(grid.lon, grid.lat[::-1], z)
    feats = []
    for lv in np.arange(np.floor(np.nanmin(s)), np.ceil(np.nanmax(s)) + 1, 1.0):
        for line in gen.lines(lv):
            if len(line) < min_pts:
                continue
            xy = np.round(line, 4)
            keep = np.r_[True, np.any(np.diff(xy, axis=0) != 0, axis=1)]
            xy = xy[keep]
            if len(xy) < min_pts:
                continue
            feats.append({"type": "Feature",
                          "properties": {"v": int(lv), "major": bool(int(lv) % 5 == 0)},
                          "geometry": {"type": "LineString", "coordinates": xy.tolist()}})
    with open(path, "w") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f, separators=(",", ":"))
    return len(feats)
