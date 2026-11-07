"""Assimilation des écarts récents des stations (Tn).

python -m src.assim [--res 150]  ->  data/history/bias.json

Pour chaque station : écart (observation - prévision recalculée avec la formule ACTUELLE, sans assimilation),
moyenné sur les nuits récentes, séparément pour les nuits radiatives (poids = indice d'inversion) et les autres
(poids = 1 - indice), avec rétrécissement vers 0 quand il y a peu de nuits. L'écart est propagé aux pixels voisins
de relief semblable (distance, profondeur de creux, altitude). Validation : l'écart appris sur les premières nuits
doit réduire l'erreur sur les dernières. Appliqué aux cartes seulement si AUTO_ASSIMILATION = True."""
import argparse, json, os
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
from . import config as C
from .archive import FORECASTS, STATIONS, EXTRA, _px
from .observe import OBS

BIAS = "data/history/bias.json"
NEED = ["tn_obs", "tn_model", "dz", "hp", "w_obs", "dz_inv", "inversion", "mistral_s", "dem_pix"]


def reconstruct(m):
    """Tn que la formule actuelle (hors assimilation) donnerait avec les champs archivés."""
    a0, a1 = C.AMP_ALT_RANGE
    f = np.clip((m.dem_pix - a0) / (a1 - a0), 0, 1)
    amp = C.AMP_LST_TO_AIR * (1 - f) + C.AMP_HIGH_ALT * f
    inv, hp = m.inversion, m.hp.fillna(0)
    return (m.tn_model + (1 - inv) * C.LAPSE_TN * m.dz
            + inv * (amp * m.w_obs * hp + (1 - m.w_obs) * C.INV_DZ_GAIN * m.dz_inv)
            + C.MISTRAL_BIAS_K * m.mistral_s)


def weight(d_m, dz1, dz2, alt1, alt2):
    L = C.ASSIM_RADIUS_KM * 1000.0
    return (np.exp(-0.5 * (d_m / L) ** 2) * np.exp(-0.5 * ((dz1 - dz2) / C.ASSIM_DZ_SCALE_M) ** 2)
            * np.exp(-0.5 * ((alt1 - alt2) / C.ASSIM_ALT_SCALE_M) ** 2))


def station_bias(d, ref_date):
    """Écart de la station : resid ~ b_rad x inv + b_non x (1 - inv), moindres carrés pondérés par l'âge des nuits
    (demi-vie ASSIM_HALF_LIFE_DAYS), rétrécis vers 0 (ASSIM_N0 nuits a priori)."""
    age = (ref_date - pd.to_datetime(d.date)).dt.days.clip(lower=0).values
    wt = 0.5 ** (age / C.ASSIM_HALF_LIFE_DAYS)
    X = np.column_stack([d.inv.values, 1 - d.inv.values])
    r = d.resid.values
    lam = C.ASSIM_N0 * np.mean(X ** 2, axis=0)
    b = np.linalg.solve(X.T @ (X * wt[:, None]) + np.diag(lam), X.T @ (wt * r))
    n = (wt[:, None] * X).sum(axis=0)                      # poids cumulé des nuits radiatives / non radiatives
    b = np.where(n >= C.ASSIM_MIN_EFF, b, 0.0)             # pas assez de nuits de ce régime : pas de correction
    return {"b_rad": float(b[0]), "b_non": float(b[1]), "n_rad": round(float(n[0]), 2), "n_non": round(float(n[1]), 2)}


def _meters(lat1, lon1, lat2, lon2):
    return np.hypot((lon1 - lon2) * 111320.0 * np.cos(np.radians(44.0)), (lat1 - lat2) * 111320.0)


def _fit_all(pairs, st, ref_date):
    rows = []
    for sid, d in pairs.groupby("id"):
        if sid not in st.index:
            continue
        b = station_bias(d, ref_date)
        last = d.sort_values("date").iloc[-1]
        rows.append(dict(id=sid, name=str(st.loc[sid, "name"]), lat=float(st.loc[sid, "lat"]), lon=float(st.loc[sid, "lon"]),
                         dem_pix=float(last.dem_pix), dz_inv=float(last.dz_inv), n_nights=int(len(d)), **b))
    return rows


def _delta(inv, lat, lon, dz, alt, bias, exclude=None):
    """Correction (K) en un point pour un indice d'inversion donné, à partir des écarts de stations."""
    num_r = num_n = den = 0.0
    for s in bias:
        if s["id"] == exclude:
            continue
        w = weight(_meters(lat, lon, s["lat"], s["lon"]), dz, s["dz_inv"], alt, s["dem_pix"])
        num_r += w * s["b_rad"]; num_n += w * s["b_non"]; den += w
    return float(np.clip(C.ASSIM_GAIN * (inv * num_r + (1 - inv) * num_n) / (den + C.ASSIM_BG_WEIGHT), -C.ASSIM_MAX_K, C.ASSIM_MAX_K))


def validate(pairs, st):
    days = sorted(pairs.date.unique())
    res = {"status": "insuffisant", "n_days": len(days)}
    if len(days) < 8:
        return res
    cut = days[int(len(days) * (1 - C.CAL_TEST_FRACTION))]
    train, test = pairs[pairs.date < cut], pairs[pairs.date >= cut]
    bias = _fit_all(train, st, pd.to_datetime(cut) - pd.Timedelta(days=1))
    byid = {b["id"]: b for b in bias}
    e0, e1, e2 = [], [], []
    for _, r in test.iterrows():
        if r.id not in byid:
            continue
        b = byid[r.id]
        own = float(np.clip(C.ASSIM_GAIN * (r.inv * b["b_rad"] + (1 - r.inv) * b["b_non"]) / (1 + C.ASSIM_BG_WEIGHT), -C.ASSIM_MAX_K, C.ASSIM_MAX_K))
        oth = _delta(r.inv, b["lat"], b["lon"], r.dz_inv, r.dem_pix, bias, exclude=r.id)
        e0.append(abs(r.resid)); e1.append(abs(r.resid - own)); e2.append(abs(r.resid - oth))
    res.update(n_test=len(e0), n_train=int(len(train)))
    if len(e0) < 15:
        return res
    m0, m1, m2 = float(np.mean(e0)), float(np.mean(e1)), float(np.mean(e2))
    res.update(mae_sans=round(m0, 3), mae_station=round(m1, 3), mae_voisines=round(m2, 3),
               gain=round((m0 - m1) / max(m0, 1e-9), 3), gain_spatial=round((m0 - m2) / max(m0, 1e-9), 3))
    res["status"] = "accepté" if res["gain"] >= C.CAL_MIN_GAIN else "rejeté (pas d'amélioration sur les nuits de validation)"
    return res


def stations_table():
    parts = [pd.read_csv(p, dtype={"id": str}) for p in (STATIONS, EXTRA) if os.path.exists(p)]
    return pd.concat(parts, ignore_index=True).drop_duplicates("id").set_index("id")


def load_pairs(res):
    f = pd.read_csv(FORECASTS, dtype={"id": str}); o = pd.read_csv(OBS, dtype={"id": str})
    m = f[f.res == res].merge(o, on=["date", "id"])
    for c in NEED:
        if c not in m.columns:
            m[c] = np.nan
    m = m.dropna(subset=NEED).copy()
    m["resid"] = m.tn_obs - reconstruct(m)
    m["inv"] = m.inversion.clip(0, 1)
    m = m[m.resid.abs() < 12]
    return m.sort_values("date").reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--res", type=int, default=150)
    a = ap.parse_args()
    if not (os.path.exists(FORECASTS) and os.path.exists(OBS)):
        print("[ASSIM] pas encore d'historique"); return
    pairs = load_pairs(a.res)
    if pairs.empty:
        print("[ASSIM] aucune nuit avec prévision et observation complètes"); return
    st = stations_table()
    ref = pd.to_datetime(pairs.date.max())
    bias = _fit_all(pairs, st, ref)
    val = validate(pairs, st)
    out = dict(updated=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), res=a.res, status=val["status"],
               applied_to_maps=bool(C.AUTO_ASSIMILATION), validation=val, stations=bias)
    os.makedirs(os.path.dirname(BIAS), exist_ok=True)
    json.dump(out, open(BIAS, "w"), indent=1, ensure_ascii=False)
    top = sorted(bias, key=lambda s: -abs(s["b_rad"]))[:6]
    print(f"[ASSIM] {len(bias)} stations, {pairs.date.nunique()} nuits ; validation : {val}")
    for s in top:
        print(f"[ASSIM]   {s['name']:<22} nuits radiatives {s['b_rad']:+.2f} K (n_eff {s['n_rad']}), autres {s['b_non']:+.2f} K (n_eff {s['n_non']})")


# ----------------------------------------------------------------- application aux cartes
def apply(tn, inv, dem, dz_inv, grid, mask):
    """Renvoie (tn corrigée, champ de correction) ou (tn, None) si inactif / non validé."""
    if not C.AUTO_ASSIMILATION:
        print("[ASSIM] assimilation inactive (AUTO_ASSIMILATION = False)", flush=True)
        return tn, None
    if not os.path.exists(BIAS):
        print("[ASSIM] active mais pas de fichier d'écarts", flush=True)
        return tn, None
    j = json.load(open(BIAS))
    if j.get("status") != "accepté" or j.get("res") != grid.res:
        print(f"[ASSIM] écarts non appliqués (statut : {j.get('status')}, résolution {j.get('res')})", flush=True)
        return tn, None
    L = C.ASSIM_RADIUS_KM * 1000.0
    R = int(3 * L / grid.res)
    num_r = np.zeros(tn.shape, np.float32); num_n = np.zeros_like(num_r); den = np.zeros_like(num_r)
    for s in j["stations"]:
        if abs(s["b_rad"]) < 1e-6 and abs(s["b_non"]) < 1e-6:
            continue
        iy, ix = _px(grid, np.array([s["lat"]]), np.array([s["lon"]]))
        y, x = int(iy[0]), int(ix[0])
        y0, y1, x0, x1 = max(y - R, 0), min(y + R + 1, grid.ny), max(x - R, 0), min(x + R + 1, grid.nx)
        yy, xx = np.mgrid[y0:y1, x0:x1]
        w = weight(np.hypot((yy - y) * grid.res, (xx - x) * grid.res), dz_inv[y0:y1, x0:x1], s["dz_inv"],
                   dem[y0:y1, x0:x1], s["dem_pix"]).astype(np.float32)
        num_r[y0:y1, x0:x1] += w * s["b_rad"]; num_n[y0:y1, x0:x1] += w * s["b_non"]; den[y0:y1, x0:x1] += w
    bg = C.ASSIM_BG_WEIGHT
    delta = np.clip(C.ASSIM_GAIN * (inv * num_r + (1 - inv) * num_n) / (den + bg), -C.ASSIM_MAX_K, C.ASSIM_MAX_K)
    delta = np.where(mask, delta, 0.0).astype(np.float32)
    print(f"[ASSIM] correction appliquée : de {delta[mask].min():+.1f} à {delta[mask].max():+.1f} K", flush=True)
    return tn + delta, delta


if __name__ == "__main__":
    main()
