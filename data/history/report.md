# Vérification Tn/Tx – stations du Gard

16 jours, 782 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 782 | +0.73 | 1.25 | +0.59 | 1.21 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 676 | +0.62 | 1.10 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 231 | +0.52 | 1.01 | +0.62 | 1.04 | +0.60 | 1.03 |
| couvert / vent fort | 36 | +0.07 | 0.68 | -0.30 | 0.56 | -0.09 | 0.51 |
| couvert / vent moyen | 189 | +0.51 | 0.87 | +0.55 | 0.86 | +0.58 | 0.87 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 16 | +0.22 | 1.40 | -0.09 | 1.08 | +0.20 | 1.28 |
| dégagé / vent moyen | 88 | +0.79 | 1.53 | +0.82 | 1.56 | +0.79 | 1.59 |
| variable / vent faible | 89 | +1.41 | 1.81 | +1.51 | 1.92 | +0.87 | 1.68 |
| variable / vent fort | 9 | -0.05 | 0.75 | -0.31 | 0.58 | +0.32 | 0.69 |
| variable / vent moyen | 69 | +0.18 | 1.24 | +0.17 | 1.25 | +0.08 | 1.19 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 300 | +0.35 | 0.96 | +0.37 | 0.97 | +0.39 | 0.92 |
| 100-300 m | 272 | +0.52 | 1.15 | +0.66 | 1.21 | +0.34 | 1.24 |
| 300-600 m | 90 | +1.74 | 2.01 | +1.62 | 1.97 | +1.45 | 1.85 |
| >600 m | 120 | +1.41 | 1.67 | +1.33 | 1.63 | +1.06 | 1.41 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 300 | -0.33 | 1.15 | -0.31 | 1.14 |
| 100-300 m | 270 | -0.45 | 1.20 | -0.29 | 1.19 |
| 300-600 m | 90 | -0.36 | 0.94 | -0.48 | 0.95 |
| >600 m | 120 | -0.84 | 1.18 | -0.92 | 1.11 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 157 | -0.62 | 1.29 | -0.59 | 1.24 |
| variable | 167 | -0.92 | 1.37 | -0.89 | 1.36 |
| couvert | 456 | -0.23 | 1.02 | -0.19 | 1.01 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 196 | -3.68 | 7.12 | -3.74 | 7.13 |
| 100-300 m | 28 | -3.79 | 8.12 | -2.63 | 8.08 |
| 300-600 m | 84 | +3.02 | 8.86 | +4.09 | 8.79 |
| >600 m | 84 | -3.69 | 12.16 | +1.34 | 11.35 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 152 | +0.99 | 8.35 | +0.87 | 7.91 |
| fort | 57 | -9.80 | 12.58 | -3.39 | 11.99 |
| moyen | 183 | -2.60 | 7.66 | -1.58 | 7.82 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 107 | +0.19 | 0.20 |
| faible (0,1-2) | 169 | +0.04 | 0.84 |
| modérée (2-10) | 132 | -3.06 | 4.56 |
| forte (>10) | 234 | -10.95 | 19.58 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **-0.8 K/km** (644 cas).
- `LAPSE_TX` ≈ **-7.4 K/km** (780 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
