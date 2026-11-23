# Vérification Tn/Tx – stations du Gard

22 jours, 1042 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1042 | +0.79 | 1.26 | +0.68 | 1.22 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 936 | +0.73 | 1.15 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 353 | +0.80 | 1.16 | +0.89 | 1.20 | +0.85 | 1.18 |
| couvert / vent fort | 53 | +0.15 | 0.70 | -0.22 | 0.53 | -0.07 | 0.49 |
| couvert / vent moyen | 246 | +0.56 | 0.91 | +0.61 | 0.92 | +0.63 | 0.93 |
| dégagé / vent faible | 55 | +2.53 | 2.69 | +2.66 | 2.80 | +1.15 | 2.37 |
| dégagé / vent fort | 20 | -0.06 | 1.36 | -0.28 | 1.07 | -0.03 | 1.22 |
| dégagé / vent moyen | 105 | +0.79 | 1.47 | +0.82 | 1.51 | +0.76 | 1.53 |
| variable / vent faible | 106 | +1.36 | 1.73 | +1.45 | 1.83 | +0.84 | 1.56 |
| variable / vent fort | 11 | +0.02 | 0.67 | -0.21 | 0.51 | +0.30 | 0.60 |
| variable / vent moyen | 93 | +0.38 | 1.31 | +0.38 | 1.34 | +0.29 | 1.24 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 400 | +0.53 | 1.06 | +0.55 | 1.07 | +0.55 | 1.02 |
| 100-300 m | 362 | +0.63 | 1.18 | +0.78 | 1.25 | +0.50 | 1.25 |
| 300-600 m | 120 | +1.63 | 1.87 | +1.52 | 1.86 | +1.36 | 1.73 |
| >600 m | 160 | +1.21 | 1.48 | +1.13 | 1.44 | +0.93 | 1.27 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 400 | -0.45 | 1.24 | -0.42 | 1.23 |
| 100-300 m | 360 | -0.53 | 1.26 | -0.37 | 1.23 |
| 300-600 m | 120 | -0.55 | 1.03 | -0.67 | 1.07 |
| >600 m | 160 | -0.92 | 1.21 | -1.00 | 1.16 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 178 | -0.69 | 1.29 | -0.65 | 1.23 |
| variable | 210 | -0.92 | 1.35 | -0.88 | 1.34 |
| couvert | 652 | -0.41 | 1.16 | -0.37 | 1.15 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 266 | -2.95 | 6.69 | -3.00 | 6.70 |
| 100-300 m | 38 | -5.05 | 8.23 | -3.77 | 7.94 |
| 300-600 m | 114 | +4.04 | 10.20 | +5.07 | 9.63 |
| >600 m | 114 | -3.11 | 10.88 | +2.44 | 11.14 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 215 | +1.03 | 8.33 | +1.05 | 7.82 |
| fort | 74 | -7.17 | 11.27 | +0.30 | 12.32 |
| moyen | 243 | -2.31 | 7.70 | -1.37 | 7.66 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 189 | +0.13 | 0.13 |
| faible (0,1-2) | 273 | -0.01 | 0.73 |
| modérée (2-10) | 197 | -2.66 | 3.78 |
| forte (>10) | 243 | -10.69 | 19.03 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.83** (régression sur 37 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+1.0 K/km** (887 cas).
- `LAPSE_TX` ≈ **-7.2 K/km** (1040 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
