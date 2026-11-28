# Vérification Tn/Tx – stations du Gard

27 jours, 1198 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1198 | +0.86 | 1.31 | +0.74 | 1.25 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 1092 | +0.81 | 1.23 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 375 | +0.83 | 1.18 | +0.92 | 1.22 | +0.87 | 1.20 |
| couvert / vent fort | 63 | +0.18 | 0.73 | -0.18 | 0.51 | -0.04 | 0.48 |
| couvert / vent moyen | 281 | +0.52 | 0.92 | +0.55 | 0.93 | +0.57 | 0.93 |
| dégagé / vent faible | 65 | +2.47 | 2.61 | +2.59 | 2.70 | +1.20 | 2.26 |
| dégagé / vent fort | 24 | +0.03 | 1.25 | -0.13 | 1.04 | +0.10 | 1.16 |
| dégagé / vent moyen | 124 | +0.84 | 1.48 | +0.88 | 1.51 | +0.77 | 1.47 |
| variable / vent faible | 134 | +1.66 | 1.96 | +1.76 | 2.06 | +1.17 | 1.75 |
| variable / vent fort | 12 | -0.05 | 0.69 | -0.22 | 0.49 | +0.26 | 0.57 |
| variable / vent moyen | 120 | +0.61 | 1.38 | +0.63 | 1.42 | +0.53 | 1.31 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 460 | +0.61 | 1.14 | +0.64 | 1.15 | +0.62 | 1.07 |
| 100-300 m | 416 | +0.73 | 1.25 | +0.87 | 1.33 | +0.59 | 1.29 |
| 300-600 m | 138 | +1.71 | 1.92 | +1.59 | 1.90 | +1.43 | 1.76 |
| >600 m | 184 | +1.14 | 1.41 | +1.06 | 1.35 | +0.88 | 1.21 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 460 | -0.49 | 1.21 | -0.46 | 1.20 |
| 100-300 m | 414 | -0.63 | 1.28 | -0.47 | 1.23 |
| 300-600 m | 138 | -0.59 | 1.03 | -0.71 | 1.06 |
| >600 m | 184 | -0.91 | 1.24 | -0.99 | 1.18 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 211 | -0.79 | 1.30 | -0.75 | 1.24 |
| variable | 266 | -0.96 | 1.33 | -0.91 | 1.29 |
| couvert | 719 | -0.44 | 1.15 | -0.40 | 1.14 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 308 | -2.67 | 6.58 | -2.72 | 6.59 |
| 100-300 m | 44 | -5.12 | 9.22 | -3.72 | 8.93 |
| 300-600 m | 132 | +4.73 | 10.55 | +5.86 | 9.94 |
| >600 m | 132 | -3.31 | 10.71 | +2.35 | 11.14 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 243 | +1.26 | 8.51 | +1.30 | 7.97 |
| fort | 85 | -6.45 | 10.67 | +1.04 | 12.02 |
| moyen | 288 | -2.15 | 7.86 | -1.13 | 7.80 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 249 | +0.18 | 0.19 |
| faible (0,1-2) | 297 | +0.05 | 0.76 |
| modérée (2-10) | 231 | -2.63 | 3.83 |
| forte (>10) | 280 | -10.34 | 17.60 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.85** (régression sur 43 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+1.3 K/km** (1006 cas).
- `LAPSE_TX` ≈ **-8.0 K/km** (1196 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
