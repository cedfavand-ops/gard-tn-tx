# Vérification Tn/Tx – stations du Gard

23 jours, 1068 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1068 | +0.80 | 1.26 | +0.69 | 1.22 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 962 | +0.74 | 1.15 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 365 | +0.81 | 1.16 | +0.90 | 1.20 | +0.86 | 1.18 |
| couvert / vent fort | 55 | +0.16 | 0.70 | -0.20 | 0.52 | -0.05 | 0.49 |
| couvert / vent moyen | 258 | +0.59 | 0.92 | +0.63 | 0.93 | +0.65 | 0.94 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 20 | -0.06 | 1.36 | -0.28 | 1.07 | -0.03 | 1.22 |
| dégagé / vent moyen | 105 | +0.79 | 1.47 | +0.82 | 1.51 | +0.76 | 1.53 |
| variable / vent faible | 106 | +1.36 | 1.73 | +1.45 | 1.83 | +0.84 | 1.56 |
| variable / vent fort | 11 | +0.02 | 0.67 | -0.21 | 0.51 | +0.30 | 0.60 |
| variable / vent moyen | 93 | +0.38 | 1.31 | +0.38 | 1.34 | +0.29 | 1.24 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 410 | +0.54 | 1.06 | +0.57 | 1.08 | +0.56 | 1.02 |
| 100-300 m | 371 | +0.64 | 1.18 | +0.79 | 1.25 | +0.52 | 1.25 |
| 300-600 m | 123 | +1.64 | 1.87 | +1.53 | 1.86 | +1.37 | 1.73 |
| >600 m | 164 | +1.19 | 1.45 | +1.11 | 1.41 | +0.92 | 1.25 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 410 | -0.47 | 1.23 | -0.44 | 1.22 |
| 100-300 m | 369 | -0.56 | 1.27 | -0.40 | 1.24 |
| 300-600 m | 123 | -0.56 | 1.03 | -0.69 | 1.07 |
| >600 m | 164 | -0.91 | 1.20 | -0.99 | 1.16 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 178 | -0.69 | 1.29 | -0.65 | 1.23 |
| variable | 210 | -0.92 | 1.35 | -0.88 | 1.34 |
| couvert | 678 | -0.44 | 1.16 | -0.40 | 1.15 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 273 | -2.88 | 6.72 | -2.93 | 6.73 |
| 100-300 m | 39 | -5.83 | 8.93 | -4.51 | 8.57 |
| 300-600 m | 117 | +4.23 | 10.50 | +5.30 | 9.80 |
| >600 m | 117 | -3.32 | 10.90 | +2.27 | 11.17 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 221 | +1.02 | 8.54 | +1.09 | 7.97 |
| fort | 76 | -7.20 | 11.19 | +0.30 | 12.24 |
| moyen | 249 | -2.36 | 7.82 | -1.43 | 7.77 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 190 | +0.13 | 0.13 |
| faible (0,1-2) | 274 | -0.01 | 0.73 |
| modérée (2-10) | 216 | -2.82 | 3.85 |
| forte (>10) | 248 | -10.65 | 18.82 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+1.0 K/km** (913 cas).
- `LAPSE_TX` ≈ **-7.2 K/km** (1066 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
