# Vérification Tn/Tx – stations du Gard

24 jours, 1094 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1094 | +0.81 | 1.26 | +0.70 | 1.21 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 988 | +0.74 | 1.16 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 365 | +0.81 | 1.16 | +0.90 | 1.20 | +0.86 | 1.18 |
| couvert / vent fort | 57 | +0.19 | 0.71 | -0.17 | 0.52 | -0.03 | 0.49 |
| couvert / vent moyen | 258 | +0.59 | 0.92 | +0.63 | 0.93 | +0.65 | 0.94 |
| dégagé / vent faible | 59 | +2.50 | 2.65 | +2.62 | 2.75 | +1.14 | 2.31 |
| dégagé / vent fort | 24 | +0.03 | 1.25 | -0.13 | 1.04 | +0.10 | 1.16 |
| dégagé / vent moyen | 118 | +0.84 | 1.48 | +0.88 | 1.51 | +0.77 | 1.49 |
| variable / vent faible | 106 | +1.36 | 1.73 | +1.45 | 1.83 | +0.84 | 1.56 |
| variable / vent fort | 12 | -0.05 | 0.69 | -0.22 | 0.49 | +0.26 | 0.57 |
| variable / vent moyen | 95 | +0.39 | 1.30 | +0.39 | 1.34 | +0.29 | 1.23 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 420 | +0.56 | 1.07 | +0.58 | 1.08 | +0.57 | 1.02 |
| 100-300 m | 380 | +0.66 | 1.19 | +0.80 | 1.26 | +0.52 | 1.25 |
| 300-600 m | 126 | +1.65 | 1.88 | +1.54 | 1.86 | +1.37 | 1.73 |
| >600 m | 168 | +1.16 | 1.43 | +1.09 | 1.39 | +0.90 | 1.23 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 420 | -0.48 | 1.23 | -0.45 | 1.22 |
| 100-300 m | 378 | -0.59 | 1.29 | -0.43 | 1.25 |
| 300-600 m | 126 | -0.58 | 1.03 | -0.70 | 1.07 |
| >600 m | 168 | -0.91 | 1.22 | -0.99 | 1.17 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 199 | -0.76 | 1.30 | -0.72 | 1.24 |
| variable | 213 | -0.93 | 1.36 | -0.89 | 1.34 |
| couvert | 680 | -0.44 | 1.16 | -0.40 | 1.15 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 280 | -2.75 | 6.68 | -2.80 | 6.69 |
| 100-300 m | 40 | -5.10 | 9.29 | -3.73 | 9.02 |
| 300-600 m | 120 | +4.37 | 10.48 | +5.47 | 9.85 |
| >600 m | 120 | -3.11 | 10.84 | +2.49 | 11.26 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 223 | +1.04 | 8.49 | +1.10 | 7.92 |
| fort | 80 | -6.55 | 11.04 | +0.80 | 12.27 |
| moyen | 257 | -2.06 | 7.87 | -1.12 | 7.86 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 213 | +0.11 | 0.12 |
| faible (0,1-2) | 276 | -0.01 | 0.73 |
| modérée (2-10) | 217 | -2.83 | 3.85 |
| forte (>10) | 248 | -10.65 | 18.82 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.84** (régression sur 39 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+1.0 K/km** (935 cas).
- `LAPSE_TX` ≈ **-7.5 K/km** (1092 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
