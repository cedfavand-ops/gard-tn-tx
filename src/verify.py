"""Compare prévisions archivées et observations des stations du Gard.
python -m src.verify  ->  data/history/report.md"""
import os
import numpy as np
import pandas as pd
from .archive import FORECASTS
from .observe import OBS

REPORT = "data/history/report.md"
MIN_N = 15     # effectif minimal pour proposer un réglage


def _cloud_cls(c):
    return pd.cut(c, [-1, 25, 70, 101], labels=["dégagé", "variable", "couvert"])


def _wind_cls(w):
    return pd.cut(w, [-1, 2, 5, 99], labels=["faible", "moyen", "fort"])


def _table(df, by, cols):
    lines = [f"| {by} | n | " + " | ".join(f"biais {c} | MAE {c}" for c in cols) + " |",
             "|" + "---|" * (2 + 2 * len(cols))]
    for k, g in df.groupby(by, observed=True):
        cells = []
        for c, ref in cols.items():
            e = (g[c] - g[ref]).dropna()
            cells += [f"{e.mean():+.2f}" if len(e) else "–", f"{e.abs().mean():.2f}" if len(e) else "–"]
        lines.append(f"| {k} | {len(g)} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    if not (os.path.exists(FORECASTS) and os.path.exists(OBS)):
        print("[VERIF] pas encore d'historique (prévisions + observations)"); return
    f = pd.read_csv(FORECASTS, dtype={"id": str}); o = pd.read_csv(OBS, dtype={"id": str})
    m = f.merge(o, on=["date", "id"])
    if m.empty:
        print("[VERIF] aucune date commune prévision / observation"); return
    m["cloud"] = m.cloud_obs.fillna(m.cloud_pred); m["wind"] = m.wind_obs.fillna(m.wind_pred)
    m["situation"] = _cloud_cls(m.cloud).astype(str) + " / vent " + _wind_cls(m.wind).astype(str)
    m["alt_cls"] = pd.cut(m.alti, [-1, 100, 300, 600, 3000], labels=["<100 m", "100-300 m", "300-600 m", ">600 m"])
    tn = m.dropna(subset=["tn_obs"]).copy(); tx = m.dropna(subset=["tx_obs"]).copy()
    for c in ("tn", "tn3", "tn_model", "tn_plain", "tn_rad"):
        tn[c + "_e"] = tn[c]
    out = [f"# Vérification Tn/Tx – stations du Gard\n", f"{m.date.nunique()} jours, {len(m)} couples station-jour. "
           "Biais = prévision − observation (°C).\n"]
    cols_tn = {"tn_model": "tn_obs", "tn_plain": "tn_obs", "tn": "tn_obs"}
    diag = []
    if {"tn_night_obs", "tn_night_model"} <= set(tn.columns):
        nn = tn.dropna(subset=["tn_night_obs", "tn_night_model"]).copy()
        if len(nn):
            diag = ["## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)\n",
                    _table(tn.assign(fenetre="18h-18h UTC"), "fenetre", {"tn_model": "tn_obs", "tn": "tn_obs"}), "",
                    _table(nn.assign(fenetre="nuit 21h-07h UTC"), "fenetre", {"tn_night_model": "tn_night_obs"}), "",
                    "Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée "
                    "ou en fin de fenêtre, pas au petit matin.\n"]
    out += diag
    out += ["## Tn par situation (conditions observées de la nuit)\n", _table(tn, "situation", cols_tn), "",
            "## Tn par classe d'altitude\n", _table(tn, "alt_cls", cols_tn), "",
            "Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.\n"]
    cols_tx = {"tx_model": "tx_obs", "tx": "tx_obs"}
    out += ["## Tx par classe d'altitude\n", _table(tx, "alt_cls", cols_tx), "",
            "## Tx par nébulosité\n", _table(tx.assign(neb=_cloud_cls(tx.cloud)), "neb", cols_tx), ""]

    if "gust_obs" in m.columns:
        gg = m.dropna(subset=["gust_obs", "gust_model"]).copy()
        if len(gg):
            gg["vent_cls"] = _wind_cls(gg.wind_obs.fillna(gg.wind_pred) if "wind_pred" in gg else gg.wind_obs).astype(str)
            cols_g = {"gust_model": "gust_obs", "gust": "gust_obs"}
            out += ["## Rafales maximales (km/h) par classe d'altitude\n", _table(gg, "alt_cls", cols_g), "",
                    "## Rafales maximales par vent nocturne observé\n", _table(gg, "vent_cls", cols_g), "",
                    "`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). "
                    "Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.\n"]
    if "rain_obs" in m.columns and "rain" in m.columns:
        rr = m.dropna(subset=["rain_obs", "rain"]).copy()
        if len(rr):
            rr["pluie_obs"] = pd.cut(rr.rain_obs, [-1, 0.1, 2, 10, 1000], labels=["sec (<0,1 mm)", "faible (0,1-2)", "modérée (2-10)", "forte (>10)"])
            out += ["## Pluie du jour civil de demain (mm) selon le cumul observé\n", _table(rr, "pluie_obs", {"rain": "rain_obs"}), "",
                    "Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.\n"]
    out.append("## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)\n")
    rad = tn[(tn.inversion >= 0.7) & (tn.wind < 2) & (tn.cloud < 25) & tn.hp.notna()]
    if len(rad) >= MIN_N and (rad.hp ** 2).sum() > 0:
        resid = rad.tn_obs - rad.tn_model
        amp = float((rad.hp * resid).sum() / (rad.hp ** 2).sum())
        out.append(f"- `AMP_LST_TO_AIR` ≈ **{amp:.2f}** (régression sur {len(rad)} cas de nuit calme et claire ; actuel : voir config).")
    else:
        out.append(f"- `AMP_LST_TO_AIR` : {len(rad)} cas de nuit calme et claire avec ECOSTRESS, il en faut au moins {MIN_N}.")
    for name, d, ref, mod in (("LAPSE_TN (nuits ventées ou couvertes)", tn[(tn.wind >= 2) | (tn.cloud >= 70)], "tn_obs", "tn_model"),
                              ("LAPSE_TX", tx, "tx_obs", "tx_model")):
        d = d.dropna(subset=["dz"])
        if len(d) >= MIN_N and (d.dz ** 2).sum() > 0:
            g = float(((d[ref] - d[mod]) * d.dz).sum() / (d.dz ** 2).sum())
            out.append(f"- `{name}` ≈ **{g * 1000:+.1f} K/km** ({len(d)} cas).")
        else:
            out.append(f"- `{name}` : {len(d)} cas, il en faut au moins {MIN_N}.")
    out.append("\nÀ valider sur des jours mis de côté avant de modifier `src/config.py`.")
    with open(REPORT, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
