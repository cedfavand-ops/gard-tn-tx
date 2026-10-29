import numpy as np
from .config import BBOX, LAT_REF


class Grid:
    """Grille régulière lon/lat dont le pas vaut ~res mètres. Ligne 0 = nord."""

    def __init__(self, res=150):
        lon0, lat0, lon1, lat1 = BBOX
        self.res = res
        self.dlat = res / 111_320.0
        self.dlon = self.dlat / np.cos(np.radians(LAT_REF))
        self.nx = int(np.ceil((lon1 - lon0) / self.dlon))
        self.ny = int(np.ceil((lat1 - lat0) / self.dlat))
        self.lon = lon0 + (np.arange(self.nx) + 0.5) * self.dlon
        self.lat = lat1 - (np.arange(self.ny) + 0.5) * self.dlat
        self.LON, self.LAT = np.meshgrid(self.lon, self.lat)
        # (ouest, sud, est, nord) exacts de la grille
        self.bounds = (lon0, lat1 - self.ny * self.dlat, lon0 + self.nx * self.dlon, lat1)
