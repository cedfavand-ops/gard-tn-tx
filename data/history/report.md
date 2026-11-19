# Vérification Tn/Tx – stations du Gard

18 jours, 886 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 886 | +0.71 | 1.22 | +0.59 | 1.18 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 780 | +0.62 | 1.09 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 296 | +0.57 | 1.00 | +0.67 | 1.04 | +0.64 | 1.02 |
| couvert / vent fort | 44 | +0.07 | 0.72 | -0.28 | 0.57 | -0.11 | 0.52 |
| couvert / vent moyen | 208 | +0.46 | 0.86 | +0.49 | 0.86 | +0.52 | 0.86 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 16 | +0.22 | 1.40 | -0.09 | 1.08 | +0.20 | 1.28 |
| dégagé / vent moyen | 88 | +0.79 | 1.53 | +0.82 | 1.56 | +0.79 | 1.59 |
| variable / vent faible | 96 | +1.39 | 1.77 | +1.48 | 1.87 | +0.86 | 1.63 |
| variable / vent fort | 9 | -0.05 | 0.75 | -0.31 | 0.58 | +0.32 | 0.69 |
| variable / vent moyen | 74 | +0.25 | 1.28 | +0.24 | 1.28 | +0.17 | 1.20 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 340 | +0.37 | 0.96 | +0.40 | 0.97 | +0.40 | 0.92 |
| 100-300 m | 308 | +0.51 | 1.11 | +0.66 | 1.17 | +0.37 | 1.19 |
| 300-600 m | 102 | +1.67 | 1.94 | +1.55 | 1.91 | +1.38 | 1.78 |
| >600 m | 136 | +1.30 | 1.60 | +1.22 | 1.56 | +0.98 | 1.36 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 340 | -0.20 | 1.13 | -0.17 | 1.12 |
| 100-300 m | 306 | -0.31 | 1.17 | -0.15 | 1.16 |
| 300-600 m | 102 | -0.33 | 0.89 | -0.45 | 0.91 |
| >600 m | 136 | -0.90 | 1.20 | -0.98 | 1.16 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 157 | -0.62 | 1.29 | -0.59 | 1.24 |
| variable | 179 | -0.82 | 1.33 | -0.79 | 1.32 |
| couvert | 548 | -0.14 | 1.01 | -0.10 | 1.01 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 224 | -3.46 | 6.75 | -3.51 | 6.76 |
| 100-300 m | 32 | -4.54 | 8.32 | -3.41 | 8.18 |
| 300-600 m | 96 | +2.59 | 8.78 | +3.58 | 8.48 |
| >600 m | 96 | -4.08 | 11.67 | +1.18 | 10.85 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 184 | +0.55 | 7.81 | +0.47 | 7.33 |
| fort | 63 | -9.43 | 12.21 | -2.46 | 11.64 |
| moyen | 201 | -2.84 | 7.64 | -1.84 | 7.71 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 135 | +0.15 | 0.16 |
| faible (0,1-2) | 203 | -0.04 | 0.78 |
| modérée (2-10) | 170 | -2.82 | 4.06 |
| forte (>10) | 238 | -10.77 | 19.29 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **-0.5 K/km** (741 cas).
- `LAPSE_TX` ≈ **-6.2 K/km** (884 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
