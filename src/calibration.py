"""Calibration prudente de AMP_LST_TO_AIR, LAPSE_TN et LAPSE_TX à partir des stations du Gard.

python -m src.calibration [--res 150]   -> écrit data/history/calibration.json (+ journal)

Principe : la carte publiée est une combinaison linéaire de champs archivés, donc l'erreur s'écrit
    obs - tn_model = (1-w)*dz*LAPSE_TN + w*hp*AMP        (Tn)
    obs - tx_model = dz*LAPSE_TX                          (Tx)
Régression ridge ramenée vers les valeurs de config.py (équivalent de CAL_MIN_N observations « a priori »),
bornes de sécurité, et validation sur les jours les plus récents mis de côté.
Rien n'est appliqué aux cartes tant que AUTO_CALIBRATION = False (le fichier n'est alors qu'une proposition)."""
import argparse, json, os
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from . import config as C
from .archive import FORECASTS
from .observe import OBS

CAL = "data/history/calibration.json"
LOG = "data/history/calibration_log.csv"


# ----------------------------------------------------------------- application aux cartes
def apply():
    """Appelée au début du calcul quotidien. Ne fait rien si AUTO_CALIBRATION est False."""
    if not C.AUTO_CALIBRATION:
        print("[CAL] calibration automatique inactive (AUTO_CALIBRATION = False)", flush=True)
        return {}
    if not os.path.exists(CAL):
        print("[CAL] active mais aucun fichier de calibration : valeurs de config.py conservées", flush=True)
        return {}
    params = json.load(open(CAL)).get("params", {})
    used = {}
    for k, v in params.items():
        if k in C.CAL_BOUNDS:
            lo, hi = C.CAL_BOUNDS[k]
            setattr(C, k, float(np.clip(v, lo, hi)))
            used[k] = getattr(C, k)
    print(f"[CAL] paramètres appliqués : {used}", flush=True)
    return used


# ----------------------------------------------------------------- ajustement
def _ridge(X, r, b0, n0):
    """Moindres carrés ramenés vers b0, avec un poids équivalent à n0 observations a priori."""
    lam = np.array([max(n0 * float(np.mean(X[:, j] ** 2)), 1e-12) for j in range(X.shape[1])])
    return np.linalg.solve(X.T @ X + np.diag(lam), X.T @ r + lam * b0)


def _clip(b, names):
    return np.array([np.clip(v, *C.CAL_BOUNDS[n]) for v, n in zip(b, names)])


def _calibrate(dates, X, r, names, b0):
    b0 = np.asarray(b0, float)
    info = {"status": "insuffisant", "n": int(len(r)), "mae_old": None, "mae_new": None}
    days = sorted(set(dates))
    if len(days) < 10:
        return b0, info
    cut = days[int(len(days) * (1 - C.CAL_TEST_FRACTION))]
    tr = np.array([d < cut for d in dates]); te = ~tr
    info.update(n_train=int(tr.sum()), n_test=int(te.sum()))
    if tr.sum() < C.CAL_MIN_N or te.sum() < C.CAL_MIN_N // 2:
        return b0, info
    b_tr = _clip(_ridge(X[tr], r[tr], b0, C.CAL_MIN_N), names)
    mae = lambda b: float(np.mean(np.abs(r[te] - X[te] @ b)))
    info["mae_old"], info["mae_new"] = round(mae(b0), 3), round(mae(b_tr), 3)
    gain = (info["mae_old"] - info["mae_new"]) / max(info["mae_old"], 1e-9)
    info["gain"] = round(gain, 3)
    if gain >= C.CAL_MIN_GAIN:
        info["status"] = "accepté"
        return _clip(_ridge(X, r, b0, C.CAL_MIN_N), names), info
    info["status"] = "rejeté (pas d'amélioration sur les jours de validation)"
    return b0, info


def load_pairs(res):
    f = pd.read_csv(FORECASTS, dtype={"id": str}); o = pd.read_csv(OBS, dtype={"id": str})
    m = f[f.res == res].merge(o, on=["date", "id"])
    return m.sort_values("date").reset_index(drop=True)


def fit(m):
    out = {}
    params = {"AMP_LST_TO_AIR": C.AMP_LST_TO_AIR, "LAPSE_TN": C.LAPSE_TN, "LAPSE_TX": C.LAPSE_TX}
    # --- Tn : on ignore les écarts aberrants (> 8 K) et les fenêtres tronquées
    d = m.dropna(subset=["tn_obs", "tn_model", "dz"]).copy()
    d = d[(~d.tn_truncated.astype(bool)) & ((d.tn_obs - d.tn_model).abs() < 8)].reset_index(drop=True)
    if len(d):
        w = d.w_blend.fillna(0).values; hp = d.hp.fillna(0).values; dz = d.dz.values
        X = np.column_stack([(1 - w) * dz, w * hp]); r = (d.tn_obs - d.tn_model).values
        names = ["LAPSE_TN", "AMP_LST_TO_AIR"]
        b, info = _calibrate(list(d.date), X, r, names, [C.LAPSE_TN, C.AMP_LST_TO_AIR])
        info["cas_ecostress"] = int((w > 0.3).sum())
        params["LAPSE_TN"], params["AMP_LST_TO_AIR"] = float(b[0]), float(b[1])
        out["tn"] = info
    # --- Tx
    d = m.dropna(subset=["tx_obs", "tx_model", "dz"]).copy()
    d = d[(d.tx_obs - d.tx_model).abs() < 8].reset_index(drop=True)
    if len(d):
        X = d[["dz"]].values; r = (d.tx_obs - d.tx_model).values
        b, info = _calibrate(list(d.date), X, r, ["LAPSE_TX"], [C.LAPSE_TX])
        params["LAPSE_TX"] = float(b[0]); out["tx"] = info
    return params, out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--res", type=int, default=150)
    a = ap.parse_args()
    if not (os.path.exists(FORECASTS) and os.path.exists(OBS)):
        print("[CAL] pas encore d'historique prévisions + observations"); return
    m = load_pairs(a.res)
    if m.empty:
        print("[CAL] aucune date commune prévision / observation"); return
    params, info = fit(m)
    res = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "res": a.res,
           "n_days": int(m.date.nunique()), "params": {k: round(v, 5) for k, v in params.items()}, **info,
           "applied_to_maps": bool(C.AUTO_CALIBRATION)}
    os.makedirs(os.path.dirname(CAL), exist_ok=True)
    json.dump(res, open(CAL, "w"), indent=1, ensure_ascii=False)
    row = pd.DataFrame([{"date": res["updated"], "n_days": res["n_days"], **res["params"],
                         "tn_status": info.get("tn", {}).get("status"), "tx_status": info.get("tx", {}).get("status")}])
    row.to_csv(LOG, mode="a", header=not os.path.exists(LOG), index=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
