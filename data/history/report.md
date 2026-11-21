# Vérification Tn/Tx – stations du Gard

20 jours, 964 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 964 | +0.80 | 1.27 | +0.69 | 1.23 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 858 | +0.73 | 1.16 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 338 | +0.76 | 1.14 | +0.86 | 1.18 | +0.82 | 1.16 |
| couvert / vent fort | 47 | +0.11 | 0.72 | -0.27 | 0.55 | -0.11 | 0.51 |
| couvert / vent moyen | 236 | +0.55 | 0.91 | +0.59 | 0.92 | +0.61 | 0.93 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 16 | +0.22 | 1.40 | -0.09 | 1.08 | +0.20 | 1.28 |
| dégagé / vent moyen | 90 | +0.83 | 1.56 | +0.86 | 1.59 | +0.83 | 1.62 |
| variable / vent faible | 97 | +1.40 | 1.78 | +1.49 | 1.87 | +0.87 | 1.63 |
| variable / vent fort | 9 | -0.05 | 0.75 | -0.31 | 0.58 | +0.32 | 0.69 |
| variable / vent moyen | 76 | +0.32 | 1.32 | +0.32 | 1.34 | +0.24 | 1.25 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 370 | +0.51 | 1.05 | +0.54 | 1.06 | +0.54 | 1.02 |
| 100-300 m | 335 | +0.63 | 1.18 | +0.78 | 1.25 | +0.50 | 1.26 |
| 300-600 m | 111 | +1.65 | 1.90 | +1.54 | 1.88 | +1.37 | 1.75 |
| >600 m | 148 | +1.25 | 1.54 | +1.17 | 1.50 | +0.96 | 1.32 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 370 | -0.32 | 1.17 | -0.29 | 1.17 |
| 100-300 m | 333 | -0.43 | 1.23 | -0.28 | 1.21 |
| 300-600 m | 111 | -0.44 | 0.96 | -0.56 | 0.98 |
| >600 m | 148 | -0.91 | 1.19 | -0.99 | 1.15 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 159 | -0.62 | 1.29 | -0.60 | 1.24 |
| variable | 182 | -0.83 | 1.33 | -0.79 | 1.32 |
| couvert | 621 | -0.32 | 1.09 | -0.28 | 1.09 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 245 | -3.14 | 6.84 | -3.19 | 6.85 |
| 100-300 m | 35 | -4.66 | 8.12 | -3.41 | 7.94 |
| 300-600 m | 105 | +3.37 | 9.66 | +4.40 | 9.19 |
| >600 m | 105 | -3.73 | 11.16 | +1.71 | 10.94 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 205 | +0.98 | 8.32 | +0.99 | 7.78 |
| fort | 66 | -8.71 | 11.94 | -1.20 | 12.25 |
| moyen | 219 | -2.71 | 7.54 | -1.74 | 7.61 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 148 | +0.15 | 0.16 |
| faible (0,1-2) | 247 | -0.01 | 0.75 |
| modérée (2-10) | 190 | -2.71 | 3.87 |
| forte (>10) | 239 | -10.74 | 19.23 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+0.7 K/km** (818 cas).
- `LAPSE_TX` ≈ **-6.7 K/km** (962 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
