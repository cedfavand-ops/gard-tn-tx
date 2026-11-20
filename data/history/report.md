# Vérification Tn/Tx – stations du Gard

19 jours, 938 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 938 | +0.79 | 1.27 | +0.67 | 1.23 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 832 | +0.71 | 1.15 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 324 | +0.73 | 1.12 | +0.83 | 1.16 | +0.79 | 1.14 |
| couvert / vent fort | 46 | +0.10 | 0.72 | -0.28 | 0.56 | -0.12 | 0.52 |
| couvert / vent moyen | 225 | +0.53 | 0.91 | +0.57 | 0.91 | +0.59 | 0.92 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 16 | +0.22 | 1.40 | -0.09 | 1.08 | +0.20 | 1.28 |
| dégagé / vent moyen | 90 | +0.83 | 1.56 | +0.86 | 1.59 | +0.83 | 1.62 |
| variable / vent faible | 97 | +1.40 | 1.78 | +1.49 | 1.87 | +0.87 | 1.63 |
| variable / vent fort | 9 | -0.05 | 0.75 | -0.31 | 0.58 | +0.32 | 0.69 |
| variable / vent moyen | 76 | +0.32 | 1.32 | +0.32 | 1.34 | +0.24 | 1.25 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 360 | +0.49 | 1.04 | +0.52 | 1.06 | +0.52 | 1.01 |
| 100-300 m | 326 | +0.61 | 1.18 | +0.76 | 1.24 | +0.47 | 1.26 |
| 300-600 m | 108 | +1.66 | 1.92 | +1.54 | 1.89 | +1.38 | 1.76 |
| >600 m | 144 | +1.26 | 1.56 | +1.18 | 1.52 | +0.96 | 1.33 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 360 | -0.29 | 1.17 | -0.27 | 1.16 |
| 100-300 m | 324 | -0.41 | 1.22 | -0.25 | 1.20 |
| 300-600 m | 108 | -0.42 | 0.95 | -0.54 | 0.98 |
| >600 m | 144 | -0.92 | 1.20 | -1.00 | 1.16 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 159 | -0.62 | 1.29 | -0.60 | 1.24 |
| variable | 182 | -0.83 | 1.33 | -0.79 | 1.32 |
| couvert | 595 | -0.28 | 1.08 | -0.24 | 1.08 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 238 | -3.41 | 6.73 | -3.46 | 6.74 |
| 100-300 m | 34 | -4.55 | 8.11 | -3.34 | 8.00 |
| 300-600 m | 102 | +2.79 | 9.14 | +3.79 | 8.72 |
| >600 m | 102 | -3.86 | 11.16 | +1.54 | 10.74 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 198 | +0.62 | 8.05 | +0.58 | 7.53 |
| fort | 65 | -9.02 | 11.95 | -1.66 | 12.00 |
| moyen | 213 | -2.87 | 7.41 | -1.88 | 7.47 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 147 | +0.15 | 0.16 |
| faible (0,1-2) | 239 | -0.03 | 0.72 |
| modérée (2-10) | 174 | -2.77 | 4.01 |
| forte (>10) | 238 | -10.77 | 19.29 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+0.4 K/km** (792 cas).
- `LAPSE_TX` ≈ **-6.6 K/km** (936 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
