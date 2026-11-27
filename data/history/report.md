# Vérification Tn/Tx – stations du Gard

26 jours, 1146 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1146 | +0.82 | 1.28 | +0.71 | 1.23 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 1040 | +0.77 | 1.19 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 375 | +0.83 | 1.18 | +0.92 | 1.22 | +0.87 | 1.20 |
| couvert / vent fort | 60 | +0.17 | 0.72 | -0.19 | 0.53 | -0.05 | 0.48 |
| couvert / vent moyen | 276 | +0.52 | 0.93 | +0.55 | 0.93 | +0.57 | 0.93 |
| dégagé / vent faible | 59 | +2.50 | 2.65 | +2.62 | 2.75 | +1.14 | 2.31 |
| dégagé / vent fort | 24 | +0.03 | 1.25 | -0.13 | 1.04 | +0.10 | 1.16 |
| dégagé / vent moyen | 118 | +0.84 | 1.48 | +0.88 | 1.51 | +0.77 | 1.49 |
| variable / vent faible | 119 | +1.54 | 1.87 | +1.63 | 1.97 | +1.05 | 1.69 |
| variable / vent fort | 12 | -0.05 | 0.69 | -0.22 | 0.49 | +0.26 | 0.57 |
| variable / vent moyen | 103 | +0.45 | 1.29 | +0.45 | 1.33 | +0.37 | 1.23 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 440 | +0.56 | 1.09 | +0.59 | 1.11 | +0.57 | 1.04 |
| 100-300 m | 398 | +0.66 | 1.21 | +0.81 | 1.28 | +0.53 | 1.27 |
| 300-600 m | 132 | +1.66 | 1.89 | +1.54 | 1.87 | +1.38 | 1.73 |
| >600 m | 176 | +1.19 | 1.45 | +1.12 | 1.40 | +0.93 | 1.24 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 440 | -0.45 | 1.20 | -0.42 | 1.19 |
| 100-300 m | 396 | -0.59 | 1.27 | -0.44 | 1.23 |
| 300-600 m | 132 | -0.58 | 1.03 | -0.71 | 1.06 |
| >600 m | 176 | -0.95 | 1.25 | -1.03 | 1.20 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 199 | -0.76 | 1.30 | -0.72 | 1.24 |
| variable | 234 | -0.91 | 1.32 | -0.87 | 1.30 |
| couvert | 711 | -0.44 | 1.15 | -0.40 | 1.14 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 294 | -2.60 | 6.64 | -2.66 | 6.64 |
| 100-300 m | 42 | -4.93 | 9.23 | -3.53 | 8.99 |
| 300-600 m | 126 | +4.41 | 10.40 | +5.48 | 9.75 |
| >600 m | 126 | -3.33 | 10.85 | +2.27 | 11.10 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 231 | +1.16 | 8.43 | +1.21 | 7.89 |
| fort | 83 | -6.49 | 10.81 | +0.73 | 11.98 |
| moyen | 274 | -2.06 | 7.92 | -1.07 | 7.81 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 215 | +0.21 | 0.21 |
| faible (0,1-2) | 279 | +0.07 | 0.80 |
| modérée (2-10) | 231 | -2.63 | 3.83 |
| forte (>10) | 280 | -10.34 | 17.60 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.84** (régression sur 39 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+1.2 K/km** (975 cas).
- `LAPSE_TX` ≈ **-7.6 K/km** (1144 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
