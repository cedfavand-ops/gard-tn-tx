"""Stations Météo-France du Gard + observations horaires (données ouvertes, licence Etalab).
python -m src.observe [--file local.csv.gz] [--backfill 0]

ATTENTION : écrit pour le format documenté des « Données climatologiques de base – horaires »
(csv ';' compressé, un fichier par département) mais jamais exécuté sur le vrai fichier depuis
l'environnement de développement. Les colonnes lues sont affichées pour faciliter l'ajustement."""
import argparse, io, os, re
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import requests
from . import config as C
from .archive import STATIONS, FORECASTS
from .timewin import gust_window_utc

DEPT = "30"
BASE = "https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/HOR/"
DATASET = "https://www.data.gouv.fr/api/1/datasets/donnees-climatologiques-de-base-horaires/"
OBS = "data/history/observations.csv"


def find_url(now):
    y = now.year
    for u in (f"{BASE}H_{DEPT}_latest-{y - 1}-{y}.csv.gz", f"{BASE}H_{DEPT}_latest-{y}-{y + 1}.csv.gz"):
        try:
            if requests.head(u, timeout=30, allow_redirects=True).status_code == 200:
                return u
        except requests.RequestException:
            pass
    ds = requests.get(DATASET, timeout=60).json()          # repli : parcours du catalogue data.gouv.fr
    res = ds.get("resources")
    if isinstance(res, dict) and "href" in res:
        res = requests.get(res["href"], params={"page_size": 200, "q": f"H_{DEPT}"}, timeout=60).json().get("data", [])
    for r in res or []:
        u = r.get("url") or r.get("latest") or ""
        if re.search(rf"H_{DEPT}_latest", u):
            return u
    raise RuntimeError("fichier horaire du Gard introuvable (nom ou catalogue modifié ?)")


def read_hourly(src):
    if os.path.exists(str(src)):
        df = pd.read_csv(src, sep=";", compression="infer", low_memory=False)
    else:
        r = requests.get(src, timeout=600); r.raise_for_status()
        df = pd.read_csv(io.BytesIO(r.content), sep=";", compression="gzip", low_memory=False)
    df.columns = [c.strip().upper() for c in df.columns]
    print(f"[OBS] {len(df)} lignes ; colonnes : {', '.join(df.columns[:40])}", flush=True)
    need = {"NUM_POSTE", "AAAAMMJJHH", "T"}
    if not need <= set(df.columns):
        raise RuntimeError(f"colonnes manquantes : {need - set(df.columns)}")
    df["time"] = pd.to_datetime(df["AAAAMMJJHH"].astype(str), format="%Y%m%d%H", utc=True)
    df["NUM_POSTE"] = df["NUM_POSTE"].astype(str).str.zfill(8)
    for c in df.columns:
        if c in ("T", "TN", "TX", "FF", "FXI", "FXI3S", "FXY", "NEB", "N", "LAT", "LON", "ALTI"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        # données douteuses (qualité 2) écartées si la colonne de qualité existe
        q = "Q" + c
        if q in df.columns and c in ("T", "TN", "TX", "FF", "FXI", "FXI3S", "FXY", "NEB", "N"):
            df.loc[pd.to_numeric(df[q], errors="coerce") == 2, c] = np.nan
    return df


def write_stations(df, path=STATIONS):
    tmax = df["time"].max()
    act = df[(df["time"] > tmax - timedelta(days=14)) & df["T"].notna()]
    g = act.groupby("NUM_POSTE").agg(name=("NOM_USUEL", "last"), lat=("LAT", "last"),
                                      lon=("LON", "last"), alti=("ALTI", "last")).reset_index()
    g = g.rename(columns={"NUM_POSTE": "id"}).dropna(subset=["lat", "lon"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    g.to_csv(path, index=False)
    print(f"[OBS] {len(g)} stations actives du Gard enregistrées", flush=True)
    return g


def _col(df, *names):
    return next((n for n in names if n in df.columns), None)


def day_obs(df, D):
    """Tn, Tx observées et conditions nocturnes pour le jour de prévision D (mêmes fenêtres que la prévision)."""
    t = lambda h: D + timedelta(hours=h)
    out = []
    tn_c = _col(df, "TN", "T"); tx_c = _col(df, "TX", "T")
    wnd, cld = _col(df, "FF"), _col(df, "NEB", "N")
    gcol = _col(df, "FXI", "FXI3S", "FXY")                       # rafale (m/s) ; on garde la première colonne disponible
    gs, ge = gust_window_utc(D)
    if df["time"].max() < t(C.TX_WINDOW[1]):
        return pd.DataFrame()                      # fenêtre pas encore complète dans le fichier
    for pid, g in df.groupby("NUM_POSTE"):
        w1 = g[(g.time >= t(C.TN_WINDOW[0])) & (g.time <= t(C.TN_WINDOW[1]))]
        w2 = g[(g.time >= t(C.TX_WINDOW[0])) & (g.time <= t(C.TX_WINDOW[1]))]
        wn = g[(g.time >= t(C.NIGHT_WINDOW[0])) & (g.time <= t(C.NIGHT_WINDOW[1]))]
        n1, n2 = w1[tn_c].notna().sum(), w2[tx_c].notna().sum()
        wg = g[(g.time > gs) & (g.time <= ge)]
        ng = int(wg[gcol].notna().sum()) if gcol else 0
        cloud = wn[cld].mean() if cld and wn[cld].notna().sum() >= 5 else np.nan
        if cld and cloud == cloud and wn[cld].max() <= 8:
            cloud *= 12.5                          # octas -> %
        out.append(dict(date=D.strftime("%Y-%m-%d"), id=pid,
                        tn_obs=w1[tn_c].min() if n1 >= 20 else np.nan, n_tn=int(n1),
                        tx_obs=w2[tx_c].max() if n2 >= 20 else np.nan, n_tx=int(n2),
                        gust_obs=wg[gcol].max() * 3.6 if gcol and ng >= 20 else np.nan, n_gust=ng,
                        wind_obs=wn[wnd].mean() if wnd and wn[wnd].notna().sum() >= 5 else np.nan,
                        cloud_obs=cloud))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=None, help="fichier horaire local (tests)")
    ap.add_argument("--backfill", type=int, default=0, help="inclure aussi les N derniers jours")
    ap.add_argument("--now", default=None)
    a = ap.parse_args()
    now = datetime.fromisoformat(a.now).replace(tzinfo=timezone.utc) if a.now else datetime.now(timezone.utc)
    df = read_hourly(a.file or find_url(now))
    write_stations(df)

    dates = set()
    if os.path.exists(FORECASTS):
        dates |= set(pd.read_csv(FORECASTS, usecols=["date"]).date)
    D0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
    dates |= {(D0 - timedelta(days=k)).strftime("%Y-%m-%d") for k in range(2, a.backfill + 2)}
    old = pd.read_csv(OBS, dtype={"id": str}) if os.path.exists(OBS) else pd.DataFrame()
    done = set(old.date) if len(old) else set()
    new = []
    for d in sorted(dates - done):
        D = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        r = day_obs(df, D)
        if len(r):
            new.append(r); print(f"[OBS] {d} : {len(r)} stations", flush=True)
    if new:
        os.makedirs(os.path.dirname(OBS), exist_ok=True)
        pd.concat([old] + new, ignore_index=True).sort_values(["date", "id"]).to_csv(OBS, index=False)


if __name__ == "__main__":
    main()
