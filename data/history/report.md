# Vérification Tn/Tx – stations du Gard

17 jours, 834 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 834 | +0.71 | 1.24 | +0.58 | 1.20 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 728 | +0.60 | 1.09 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 255 | +0.52 | 1.00 | +0.63 | 1.03 | +0.59 | 1.02 |
| couvert / vent fort | 42 | -0.00 | 0.68 | -0.33 | 0.56 | -0.16 | 0.51 |
| couvert / vent moyen | 202 | +0.47 | 0.87 | +0.50 | 0.87 | +0.53 | 0.88 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 16 | +0.22 | 1.40 | -0.09 | 1.08 | +0.20 | 1.28 |
| dégagé / vent moyen | 88 | +0.79 | 1.53 | +0.82 | 1.56 | +0.79 | 1.59 |
| variable / vent faible | 93 | +1.39 | 1.79 | +1.49 | 1.88 | +0.85 | 1.65 |
| variable / vent fort | 9 | -0.05 | 0.75 | -0.31 | 0.58 | +0.32 | 0.69 |
| variable / vent moyen | 74 | +0.25 | 1.28 | +0.24 | 1.28 | +0.17 | 1.20 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 320 | +0.35 | 0.96 | +0.37 | 0.97 | +0.38 | 0.92 |
| 100-300 m | 290 | +0.52 | 1.14 | +0.66 | 1.20 | +0.35 | 1.22 |
| 300-600 m | 96 | +1.69 | 1.98 | +1.58 | 1.96 | +1.40 | 1.82 |
| >600 m | 128 | +1.29 | 1.61 | +1.21 | 1.57 | +0.96 | 1.36 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 320 | -0.26 | 1.14 | -0.23 | 1.14 |
| 100-300 m | 288 | -0.38 | 1.18 | -0.22 | 1.16 |
| 300-600 m | 96 | -0.32 | 0.91 | -0.44 | 0.92 |
| >600 m | 128 | -0.91 | 1.22 | -0.99 | 1.17 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 157 | -0.62 | 1.29 | -0.59 | 1.24 |
| variable | 176 | -0.85 | 1.34 | -0.82 | 1.33 |
| couvert | 499 | -0.18 | 1.02 | -0.14 | 1.02 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 210 | -3.59 | 6.90 | -3.65 | 6.91 |
| 100-300 m | 30 | -4.59 | 8.62 | -3.46 | 8.55 |
| 300-600 m | 90 | +2.60 | 8.84 | +3.64 | 8.67 |
| >600 m | 90 | -3.67 | 11.77 | +1.47 | 11.09 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 164 | +0.82 | 8.00 | +0.68 | 7.58 |
| fort | 61 | -9.25 | 12.13 | -2.65 | 11.73 |
| moyen | 195 | -2.87 | 7.75 | -1.85 | 7.84 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 133 | +0.15 | 0.16 |
| faible (0,1-2) | 193 | +0.01 | 0.77 |
| modérée (2-10) | 134 | -3.05 | 4.52 |
| forte (>10) | 234 | -10.95 | 19.58 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **-0.6 K/km** (692 cas).
- `LAPSE_TX` ≈ **-6.8 K/km** (832 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
