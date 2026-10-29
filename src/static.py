"""Données statiques : MNT, masque du Gard, structure fine ECOSTRESS.
Calculées une fois par résolution, puis mises en cache dans data/static_<res>.npz."""
import json, os
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from . import config as C


# ---------- ECOSTRESS ----------
def read_ecostress(path):
    """GeoTIFF LST (uint16, K x 0.02, nodata 0) -> (°C, (x0, y0, dx, dy)). Sans GDAL/rasterio."""
    from PIL import Image
    import tifffile
    Image.MAX_IMAGE_PIXELS = None
    with tifffile.TiffFile(path) as t:
        tags = t.pages[0].tags
        sx, sy, _ = tags["ModelPixelScaleTag"].value
        _, _, _, x0, y0, _ = tags["ModelTiepointTag"].value
    a = np.asarray(Image.open(path), dtype=np.float32)
    a[a == 0] = np.nan
    return a * 0.02 - 273.15, (x0, y0, sx, sy)


def _resample(T, geo, grid):
    x0, y0, sx, sy = geo
    ok = np.isfinite(T)
    v, w = np.where(ok, T, 0).astype(np.float32), ok.astype(np.float32)
    k = grid.dlat / sy                      # facteur de réduction (~2 à 150 m, ~1 à 70 m)
    if k > 1.2:
        v, w = gaussian_filter(v, 0.5 * k), gaussian_filter(w, 0.5 * k)
    cols = (grid.LON - x0) / sx - 0.5
    rows = (y0 - grid.LAT) / sy - 0.5
    vv = map_coordinates(v, [rows, cols], order=1, cval=0.0)
    ww = map_coordinates(w, [rows, cols], order=1, cval=0.0)
    return np.where(ww > 0.5, vv / np.maximum(ww, 1e-6), np.nan).astype(np.float32)


def norm_gauss(a, sigma):
    ok = np.isfinite(a)
    v = gaussian_filter(np.where(ok, a, 0).astype(np.float32), sigma)
    w = gaussian_filter(ok.astype(np.float32), sigma)
    return np.where(w > 0.4, v / np.maximum(w, 1e-6), np.nan), w


def ecostress_highpass(grid, mask):
    lst = np.full((grid.ny, grid.nx), np.nan, np.float32)
    for p in C.ECOSTRESS_FILES:                      # priorité au premier fichier
        T, geo = read_ecostress(p)
        r = _resample(T, geo, grid)
        lst = np.where(np.isfinite(lst), lst, r)
    lst[~mask] = np.nan                              # exclut mer et hors-département
    smooth, _ = norm_gauss(lst, C.HP_SIGMA_M / grid.res)
    hp = lst - smooth
    return np.clip(hp, -C.HP_CLIP, C.HP_CLIP).astype(np.float32)


# ---------- MNT et masque ----------
def load_dem(grid):
    """Copernicus GLO-30 (AWS open data), moyenné sur la grille."""
    import rasterio
    from rasterio.transform import from_origin
    from rasterio.warp import reproject, Resampling
    lon0, lat0, lon1, lat1 = C.BBOX
    dst = np.full((grid.ny, grid.nx), np.nan, np.float32)
    tr = from_origin(grid.bounds[0], grid.bounds[3], grid.dlon, grid.dlat)
    for la in range(int(np.floor(lat0)), int(np.floor(lat1)) + 1):
        for lo in range(int(np.floor(lon0)), int(np.floor(lon1)) + 1):
            name = f"Copernicus_DSM_COG_10_N{la:02d}_00_E{lo:03d}_00_DEM"
            url = f"/vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"
            tmp = np.full(dst.shape, np.nan, np.float32)
            with rasterio.open(url) as src:
                reproject(rasterio.band(src, 1), tmp, dst_transform=tr, dst_crs="EPSG:4326",
                          resampling=Resampling.average, dst_nodata=np.nan)
            dst = np.where(np.isfinite(tmp), tmp, dst)
    return np.nan_to_num(dst, nan=0.0)


def department_mask(grid, cache="data/gard_contour.json"):
    import requests
    from matplotlib.path import Path
    if not os.path.exists(cache):
        r = requests.get("https://geo.api.gouv.fr/departements/30?fields=nom,contour", timeout=60)
        r.raise_for_status()
        with open(cache, "w") as f:
            json.dump(r.json()["contour"], f)
    g = json.load(open(cache))
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    mask = np.zeros((grid.ny, grid.nx), bool)
    pts = np.column_stack([grid.LON.ravel(), grid.LAT.ravel()])
    for poly in polys:
        m = Path(np.array(poly[0])).contains_points(pts)
        for hole in poly[1:]:
            m &= ~Path(np.array(hole)).contains_points(pts)
        mask |= m.reshape(mask.shape)
    return mask


# ---------- Démo (sans réseau) ----------
def demo_dem_mask(grid):
    z = 150 + 700 * np.exp(-(((grid.LON - 3.6) / .25) ** 2 + ((grid.LAT - 44.2) / .2) ** 2)) \
        + 120 * np.sin(grid.LON * 25) * np.cos(grid.LAT * 30)
    mask = ((grid.LON - 4.05) / 0.8) ** 2 + ((grid.LAT - 43.95) / 0.5) ** 2 < 1
    return np.clip(z, 0, None).astype(np.float32), mask


def get_static(grid, demo=False):
    path = f"data/static_{grid.res}{'_demo' if demo else ''}.npz"
    if os.path.exists(path):
        d = np.load(path)
        return d["dem"], d["mask"], d["hp"]
    dem, mask = demo_dem_mask(grid) if demo else (load_dem(grid), department_mask(grid))
    hp = ecostress_highpass(grid, mask)
    np.savez_compressed(path, dem=dem, mask=mask, hp=hp)
    return dem, mask, hp
