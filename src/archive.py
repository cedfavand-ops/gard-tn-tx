"""Archive quotidienne des prévisions aux points des stations du Gard."""
import os
import numpy as np
import pandas as pd

STATIONS = "data/stations_gard.csv"
FORECASTS = "data/history/forecasts.csv"


def _px(grid, lat, lon):
    iy = np.clip(((grid.bounds[3] - lat) / grid.dlat).astype(int), 0, grid.ny - 1)
    ix = np.clip(((lon - grid.bounds[0]) / grid.dlon).astype(int), 0, grid.nx - 1)
    return iy, ix


def _mean3(a, iy, ix):
    out = []
    for y, x in zip(iy, ix):
        blk = a[max(y - 1, 0):y + 2, max(x - 1, 0):x + 2]
        out.append(np.nanmean(blk) if np.isfinite(blk).any() else np.nan)
    return np.array(out)


def record_forecast(D, icon, grid, tn, tx, info, dem, demo=False, stations_path=STATIONS, out_path=FORECASTS):
    if (demo or icon.demo) and os.environ.get("FORCE_ARCHIVE") != "1":
        return                                  # on n'archive jamais de données synthétiques
    if not os.path.exists(stations_path):
        print("[ARCHIVE] pas de liste de stations : archivage ignoré", flush=True)
        return
    st = pd.read_csv(stations_path, dtype={"id": str})
    iy, ix = _px(grid, st.lat.values, st.lon.values)
    F = info["fields"]
    rows = pd.DataFrame({
        "date": D.strftime("%Y-%m-%d"), "id": st.id, "name": st.name, "alti": st.alti,
        "res": grid.res, "run": icon.run.strftime("%Y-%m-%dT%HZ"),
        "dem_pix": dem[iy, ix].round(1),
        "dz": F["dz"][iy, ix].round(1),                     # écart au relief « vu » par le modèle
        "hp": F["hp"][iy, ix].round(2),                      # anomalie ECOSTRESS au pixel (NaN si non observé)
        "w_blend": F["w"][iy, ix].round(2),
        "tn": tn[iy, ix].round(2), "tn3": _mean3(tn, iy, ix).round(2),
        "tn_model": F["tn_model"][iy, ix].round(2), "tn_plain": F["tn_plain"][iy, ix].round(2),
        "tn_rad": F["tn_rad"][iy, ix].round(2),
        "tx": tx[iy, ix].round(2), "tx3": _mean3(tx, iy, ix).round(2),
        "tx_model": F["tx_model"][iy, ix].round(2),
        "inversion": F["inv"][iy, ix].round(2),                       # indice d'inversion au pixel de la station
        "wind_pred": F["wind_night"][iy, ix].round(1), "cloud_pred": F["cloud_night"][iy, ix].round(0),
        "tn_truncated": info["tn_truncated"], "tx_truncated": info["tx_truncated"],
        "gust": F["gust"][iy, ix].round(1) if "gust" in F else np.nan,              # km/h
        "gust_model": F["gust_model"][iy, ix].round(1) if "gust_model" in F else np.nan,
        "gust_factor": F["gust_factor"][iy, ix].round(2) if "gust_factor" in F else np.nan,
    })
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path):
        old = pd.read_csv(out_path, dtype={"id": str})
        keys = set(zip(rows.date, rows.id, rows.res))
        old = old[[(d, i, r) not in keys for d, i, r in zip(old.date, old.id, old.res)]]
        rows = pd.concat([old, rows], ignore_index=True)
    rows.sort_values(["date", "id", "res"]).to_csv(out_path, index=False)
    print(f"[ARCHIVE] {len(st)} stations enregistrées pour le {D:%Y-%m-%d}", flush=True)
