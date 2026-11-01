"""Isolignes GeoJSON : fines tous les 1 °C, épaisses (major) tous les 5 °C."""
import json
import numpy as np
from contourpy import contour_generator
from .static import norm_gauss


def isolines(a, grid, path, minor=1.0, major=5.0, levels=None, major_levels=(), smooth_m=225.0, min_pts=8):
    s, _ = norm_gauss(a, smooth_m / grid.res)        # lissage tenant compte des NaN
    z = np.ma.masked_invalid(s[::-1])                 # latitudes croissantes
    gen = contour_generator(grid.lon, grid.lat[::-1], z)
    feats = []
    if levels is None:
        levels = np.arange(np.floor(np.nanmin(s) / minor) * minor, np.ceil(np.nanmax(s) / minor) * minor + minor, minor)
        is_major = lambda lv: bool(abs(lv / major - round(lv / major)) < 1e-6)
    else:
        is_major = lambda lv: any(abs(lv - m) < 1e-9 for m in major_levels)
    for lv in levels:
        for line in gen.lines(lv):
            if len(line) < min_pts:
                continue
            xy = np.round(line, 4)
            keep = np.r_[True, np.any(np.diff(xy, axis=0) != 0, axis=1)]
            xy = xy[keep]
            if len(xy) < min_pts:
                continue
            feats.append({"type": "Feature",
                          "properties": {"v": float(lv), "major": is_major(lv)},
                          "geometry": {"type": "LineString", "coordinates": xy.tolist()}})
    with open(path, "w") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f, separators=(",", ":"))
    return len(feats)
