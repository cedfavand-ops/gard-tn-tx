"""Lecture d'ICON-CH1-EPS (MeteoSwiss OGD) ou génération de données de démonstration."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import inspect
import numpy as np
from . import config as C


@dataclass
class IconData:
    run: datetime
    times: list          # instants de validité (UTC)
    lon: np.ndarray      # (npts,)
    lat: np.ndarray
    t2m: np.ndarray      # (nt, npts) °C
    wind: np.ndarray     # (nt_night, npts) m/s  -> aligné sur night_times
    cloud: np.ndarray    # (nt_night, npts) %
    night_times: list
    demo: bool = False
    sel: object = None            # masque des points ICON retenus (pour relire d'autres variables)
    gust: object = None           # (nt, npts) rafales VMAX_10M en m/s, NaN si échéance manquante
    gust_times: object = None
    uv_times: object = None       # échéances (toutes les 3 h) du vent moyen pour la direction
    u10: object = None
    v10: object = None


def day_start(now):
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


# ------------------------------------------------------------------ DÉMO
def demo_icon(now, seed=1):
    rng = np.random.default_rng(seed)
    lon0, lat0, lon1, lat1 = C.BBOX
    n = 5000
    lon = rng.uniform(lon0 - .1, lon1 + .1, n)
    lat = rng.uniform(lat0 - .1, lat1 + .1, n)
    z = 150 + 600 * np.exp(-(((lon - 3.6) / .25) ** 2 + ((lat - 44.2) / .2) ** 2))
    D = day_start(now)
    run = D - timedelta(hours=12)  # run de la veille 12 UTC, par ex.
    run = D.replace(hour=12) if now.hour >= 15 else D.replace(hour=9)
    times = [D + timedelta(hours=h) for h in range(min(C.TN_WINDOW[0], C.TX_WINDOW[0]), max(C.TN_WINDOW[1], C.TX_WINDOW[1]) + 1)
             if (D + timedelta(hours=h) - run).total_seconds() <= 33 * 3600]
    h = np.array([t.hour + 24 * (t.day != D.day) for t in times], float)
    diurnal = 4.5 * np.cos((h - 14) * 2 * np.pi / 24)          # max 14 h, min 2 h
    t2m = 6 - 0.0065 * z[None, :] + diurnal[:, None] + 0.3 * rng.standard_normal((1, n))
    nt = [t for t in times if C.NIGHT_WINDOW[0] <= (t - D).total_seconds() / 3600 <= C.NIGHT_WINDOW[1]]
    wind = np.full((len(nt), n), 1.3) + 0.2 * rng.standard_normal((len(nt), n))
    cloud = np.full((len(nt), n), 39.0)
    from .timewin import gust_valid_times
    gt = gust_valid_times(D)
    hh = np.array([(t - gt[0]).total_seconds() / 3600 for t in gt])
    amp = 11 + 7 * np.cos((hh - 12) * 2 * np.pi / 24)            # m/s, maximum en milieu de journée
    gust = amp[:, None] * (1 + 0.5 * np.exp(-(((lon - 3.6) / .3) ** 2 + ((lat - 44.2) / .25) ** 2)))[None, :] \
        + rng.normal(0, 0.5, (len(gt), n))
    uvt = gt[::3]
    w = (amp[::3] * 0.55)[:, None] * np.ones((1, n))
    phi = np.radians(330.0)                                     # mistral (vent de nord-nord-ouest)
    u10, v10 = -w * np.sin(phi), -w * np.cos(phi)
    return IconData(run, times, lon, lat, t2m, wind, cloud, nt, demo=True,
                    gust=gust, gust_times=gt, uv_times=uvt, u10=u10, v10=v10)


# ------------------------------------------------------------------ RÉEL
# ATTENTION : cette partie n'a pas pu être testée avec le vrai service depuis l'environnement de
# développement (pas d'accès réseau). Si vous avez déjà un code qui lit ICON-CH1 pour la Lozère,
# remplacez simplement fetch_icon() par lui : il doit renvoyer un IconData.
COLL = "ogd-forecasting-icon-ch1"


def _request(ogd_api, var, run, lead_h):
    """Compatible avec les différentes signatures de ogd_api.Request selon la version."""
    params = inspect.signature(ogd_api.Request).parameters
    kw = dict(collection=COLL, variable=var, perturbed=False)
    kw["reference_datetime" if "reference_datetime" in params else "ref_time"] = run
    kw["horizon" if "horizon" in params else "lead_time"] = timedelta(hours=lead_h)
    return ogd_api.Request(**kw)


_COORD_NAMES = (("lon", "lat"), ("longitude", "latitude"), ("clon", "clat"), ("CLON", "CLAT"))
_GRID = {}


def _coords(ogd_api, da, run):
    for a, b in _COORD_NAMES:
        if a in da.coords and b in da.coords:
            return np.asarray(da.coords[a].values).ravel(), np.asarray(da.coords[b].values).ravel()
    if "grid" in _GRID:                       # déjà récupérée par une autre voie
        return _GRID["grid"]
    try:                                      # repli : champs de coordonnées des cellules
        lo = ogd_api.get_from_ogd(_request(ogd_api, "CLON", run, 0))
        la = ogd_api.get_from_ogd(_request(ogd_api, "CLAT", run, 0))
        _GRID["grid"] = (np.asarray(lo.values).ravel(), np.asarray(la.values).ravel())
        return _GRID["grid"]
    except Exception as e:
        raise KeyError(f"coordonnées introuvables : dims={da.dims}, coords={list(da.coords)}, "
                       f"repli CLON/CLAT en échec : {e!r}")


def _field(ogd_api, var, run, lead_h):
    da = ogd_api.get_from_ogd(_request(ogd_api, var, run, lead_h))
    vals = np.asarray(da.values).astype(np.float64).ravel()
    lon, lat = _coords(ogd_api, da, run)
    lon, lat = lon.astype(np.float64), lat.astype(np.float64)
    if np.nanmax(np.abs(lat)) < 6.3:        # radians -> degrés
        lon, lat = np.degrees(lon), np.degrees(lat)
    if vals.size != lon.size:
        raise ValueError(f"{var}: {vals.size} valeurs pour {lon.size} coordonnées (dims={da.dims})")
    return vals, lon, lat


def _import_ogd():
    try:
        from meteodatalab import ogd_api          # nom réel du module (paquet PyPI : meteodata-lab)
    except ImportError:
        from meteodata_lab import ogd_api         # au cas où une version l'aurait renommé
    return ogd_api


def fetch_icon(now):
    ogd_api = _import_ogd()
    D = day_start(now)
    lon0, lat0, lon1, lat1 = C.BBOX
    t_first = D + timedelta(hours=C.TN_WINDOW[0])
    # runs candidats : du plus récent au plus ancien (OGD ne garde que ~24 h)
    r = (now - timedelta(hours=2)).replace(minute=0, second=0, microsecond=0)
    r = r.replace(hour=r.hour - r.hour % 3)
    last_err = None
    for k in range(8):
        run = r - timedelta(hours=3 * k)
        try:
            lead0 = int((t_first - run).total_seconds() // 3600)
            _field(ogd_api, "T_2M", run, max(lead0, 0))
        except Exception as e:           # run pas (encore) disponible, ou erreur de lecture
            last_err = e
            print(f"Run {run:%Y-%m-%d %H}Z écarté : {e!r}")
            continue
        return _fetch_run(ogd_api, run, D)
    raise RuntimeError(f"Aucun run ICON-CH1 disponible : {last_err}")


def _fetch_run(ogd_api, run, D):
    lon0, lat0, lon1, lat1 = C.BBOX
    sel, lon, lat = None, None, None
    times, t2m, ntimes, wind, cloud = [], [], [], [], []
    for h in range(min(C.TN_WINDOW[0], C.TX_WINDOW[0]), max(C.TN_WINDOW[1], C.TX_WINDOW[1]) + 1):
        t = D + timedelta(hours=h)
        lead = int((t - run).total_seconds() // 3600)
        if lead < 0:
            continue
        try:
            v, lo, la = _field(ogd_api, "T_2M", run, lead)
            if sel is None:
                sel = (lo > lon0 - .1) & (lo < lon1 + .1) & (la > lat0 - .1) & (la < lat1 + .1)
                lon, lat = lo[sel], la[sel]
            t2m.append(v[sel] - 273.15)
            times.append(t)
            print(f"[ICON] run {run:%d/%m %H}Z, +{lead} h (valide {t:%d/%m %H}Z) : T_2M ok", flush=True)
            if C.NIGHT_WINDOW[0] <= h <= C.NIGHT_WINDOW[1]:
                u = _field(ogd_api, "U_10M", run, lead)[0][sel]
                w = _field(ogd_api, "V_10M", run, lead)[0][sel]
                c = _field(ogd_api, "CLCT", run, lead)[0][sel]
                wind.append(np.hypot(u, w)); cloud.append(c); ntimes.append(t)
                print(f"[ICON]   +{lead} h : vent et nébulosité ok", flush=True)
        except Exception as e:           # au-delà de l'horizon du run : fenêtre tronquée
            print(f"Arrêt à +{lead} h : {e!r}")
            break
    print(f"[ICON] terminé : {len(times)} échéances de température, {len(ntimes)} nocturnes", flush=True)
    icon = IconData(run, times, lon, lat, np.array(t2m), np.array(wind), np.array(cloud), ntimes, sel=sel)
    try:
        _fetch_gust(ogd_api, icon, run, D)
    except Exception as e:                       # les rafales ne doivent jamais bloquer les cartes de température
        print(f"[ICON] rafales indisponibles : {e!r}", flush=True)
        icon.gust = None
    return icon


def _get_any(ogd_api, var, runs, valid, sel):
    """Lit une variable à l'échéance `valid` dans le premier run qui la fournit (run principal puis run de 03 UTC, 45 h)."""
    for run in runs:
        lead = int((valid - run).total_seconds() // 3600)
        if lead < 0:
            continue
        try:
            return _field(ogd_api, var, run, lead)[0][sel]
        except Exception:
            continue
    return None


def _fetch_gust(ogd_api, icon, run, D):
    from .timewin import gust_valid_times
    alt = D.replace(hour=3)                                  # le run de 03 UTC va jusqu'à +45 h : couvre la fin de la journée
    runs = [run] + ([alt] if alt != run else [])
    gt = gust_valid_times(D)
    npts = icon.lon.size
    gust = np.full((len(gt), npts), np.nan)
    for k, t in enumerate(gt):
        v = _get_any(ogd_api, "VMAX_10M", runs, t, icon.sel)
        if v is not None:
            gust[k] = v
            print(f"[ICON] rafales {t:%d/%m %H}Z ok", flush=True)
    if not np.isfinite(gust).any():
        raise RuntimeError("VMAX_10M introuvable")
    uvt, u, v = [], [], []
    for t in gt[::3]:
        uu = _get_any(ogd_api, "U_10M", runs, t, icon.sel)
        vv = _get_any(ogd_api, "V_10M", runs, t, icon.sel)
        if uu is not None and vv is not None:
            uvt.append(t); u.append(uu); v.append(vv)
    if not uvt:
        raise RuntimeError("U_10M / V_10M introuvables pour la direction du vent")
    icon.gust, icon.gust_times = gust, gt
    icon.uv_times, icon.u10, icon.v10 = uvt, np.array(u), np.array(v)
