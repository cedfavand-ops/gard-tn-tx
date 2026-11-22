# Vérification Tn/Tx – stations du Gard

21 jours, 1016 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1016 | +0.78 | 1.26 | +0.67 | 1.22 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 910 | +0.71 | 1.15 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 340 | +0.76 | 1.14 | +0.86 | 1.17 | +0.82 | 1.16 |
| couvert / vent fort | 51 | +0.15 | 0.71 | -0.22 | 0.54 | -0.07 | 0.50 |
| couvert / vent moyen | 238 | +0.55 | 0.91 | +0.59 | 0.92 | +0.61 | 0.93 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 20 | -0.06 | 1.36 | -0.28 | 1.07 | -0.03 | 1.22 |
| dégagé / vent moyen | 105 | +0.79 | 1.47 | +0.82 | 1.51 | +0.76 | 1.53 |
| variable / vent faible | 103 | +1.38 | 1.74 | +1.48 | 1.84 | +0.85 | 1.57 |
| variable / vent fort | 11 | +0.02 | 0.67 | -0.21 | 0.51 | +0.30 | 0.60 |
| variable / vent moyen | 93 | +0.38 | 1.31 | +0.38 | 1.34 | +0.29 | 1.24 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 390 | +0.52 | 1.06 | +0.54 | 1.07 | +0.54 | 1.02 |
| 100-300 m | 353 | +0.62 | 1.18 | +0.76 | 1.25 | +0.48 | 1.26 |
| 300-600 m | 117 | +1.61 | 1.85 | +1.49 | 1.84 | +1.33 | 1.71 |
| >600 m | 156 | +1.21 | 1.48 | +1.13 | 1.44 | +0.93 | 1.27 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 390 | -0.39 | 1.19 | -0.36 | 1.18 |
| 100-300 m | 351 | -0.46 | 1.21 | -0.31 | 1.19 |
| 300-600 m | 117 | -0.49 | 0.99 | -0.62 | 1.02 |
| >600 m | 156 | -0.88 | 1.19 | -0.96 | 1.13 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 178 | -0.69 | 1.29 | -0.65 | 1.23 |
| variable | 207 | -0.88 | 1.32 | -0.84 | 1.31 |
| couvert | 629 | -0.32 | 1.09 | -0.28 | 1.09 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 259 | -3.12 | 6.77 | -3.17 | 6.78 |
| 100-300 m | 37 | -5.08 | 8.35 | -3.80 | 8.08 |
| 300-600 m | 111 | +3.85 | 10.18 | +4.90 | 9.57 |
| >600 m | 111 | -3.30 | 10.98 | +2.29 | 11.17 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 207 | +0.83 | 8.39 | +0.84 | 7.85 |
| fort | 72 | -7.49 | 11.47 | +0.04 | 12.39 |
| moyen | 239 | -2.37 | 7.74 | -1.42 | 7.71 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 188 | +0.12 | 0.13 |
| faible (0,1-2) | 253 | -0.00 | 0.75 |
| modérée (2-10) | 192 | -2.71 | 3.86 |
| forte (>10) | 243 | -10.69 | 19.03 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+0.7 K/km** (864 cas).
- `LAPSE_TX` ≈ **-6.8 K/km** (1014 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
