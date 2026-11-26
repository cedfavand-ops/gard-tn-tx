# Vérification Tn/Tx – stations du Gard

25 jours, 1120 couples station-jour. Biais = prévision − observation (°C).

## Diagnostic de fenêtre : Tn 18 h -> 18 h UTC contre Tn de nuit (21 h -> 07 h UTC)

| fenetre | n | biais tn_model | MAE tn_model | biais tn | MAE tn |
|---|---|---|---|---|---|
| 18h-18h UTC | 1120 | +0.85 | 1.29 | +0.73 | 1.24 |

| fenetre | n | biais tn_night_model | MAE tn_night_model |
|---|---|---|---|
| nuit 21h-07h UTC | 1014 | +0.79 | 1.19 |

Si l'erreur sur 18 h-18 h est nettement plus forte que sur la nuit, le minimum du modèle tombe en soirée ou en fin de fenêtre, pas au petit matin.

## Tn par situation (conditions observées de la nuit)

| situation | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| couvert / vent faible | 371 | +0.84 | 1.19 | +0.94 | 1.23 | +0.89 | 1.20 |
| couvert / vent fort | 57 | +0.19 | 0.71 | -0.17 | 0.52 | -0.03 | 0.49 |
| couvert / vent moyen | 260 | +0.60 | 0.93 | +0.64 | 0.94 | +0.66 | 0.94 |
| dégagé / vent faible | 59 | +2.50 | 2.65 | +2.62 | 2.75 | +1.14 | 2.31 |
| dégagé / vent fort | 24 | +0.03 | 1.25 | -0.13 | 1.04 | +0.10 | 1.16 |
| dégagé / vent moyen | 118 | +0.84 | 1.48 | +0.88 | 1.51 | +0.77 | 1.49 |
| variable / vent faible | 118 | +1.54 | 1.87 | +1.63 | 1.97 | +1.05 | 1.70 |
| variable / vent fort | 12 | -0.05 | 0.69 | -0.22 | 0.49 | +0.26 | 0.57 |
| variable / vent moyen | 101 | +0.43 | 1.29 | +0.43 | 1.33 | +0.35 | 1.23 |

## Tn par classe d'altitude

| alt_cls | n | biais tn_model | MAE tn_model | biais tn_plain | MAE tn_plain | biais tn | MAE tn |
|---|---|---|---|---|---|---|---|
| <100 m | 430 | +0.59 | 1.10 | +0.62 | 1.11 | +0.61 | 1.05 |
| 100-300 m | 389 | +0.70 | 1.22 | +0.84 | 1.29 | +0.56 | 1.27 |
| 300-600 m | 129 | +1.70 | 1.92 | +1.58 | 1.90 | +1.42 | 1.76 |
| >600 m | 172 | +1.20 | 1.46 | +1.12 | 1.41 | +0.93 | 1.25 |

Colonnes : `tn_model` = valeur brute ICON ; `tn_plain` = corrigée de l'altitude seule ; `tn` = carte publiée.

## Tx par classe d'altitude

| alt_cls | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| <100 m | 430 | -0.47 | 1.21 | -0.44 | 1.20 |
| 100-300 m | 387 | -0.58 | 1.27 | -0.43 | 1.24 |
| 300-600 m | 129 | -0.58 | 1.03 | -0.70 | 1.07 |
| >600 m | 172 | -0.91 | 1.21 | -0.99 | 1.17 |

## Tx par nébulosité

| neb | n | biais tx_model | MAE tx_model | biais tx | MAE tx |
|---|---|---|---|---|---|
| dégagé | 199 | -0.76 | 1.30 | -0.72 | 1.24 |
| variable | 231 | -0.88 | 1.30 | -0.84 | 1.28 |
| couvert | 688 | -0.44 | 1.16 | -0.40 | 1.15 |

## Rafales maximales (km/h) par classe d'altitude

| alt_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| <100 m | 287 | -2.65 | 6.63 | -2.70 | 6.64 |
| 100-300 m | 41 | -5.21 | 9.30 | -3.83 | 8.99 |
| 300-600 m | 123 | +4.55 | 10.51 | +5.61 | 9.89 |
| >600 m | 123 | -3.28 | 10.93 | +2.36 | 11.20 |

## Rafales maximales par vent nocturne observé

| vent_cls | n | biais gust_model | MAE gust_model | biais gust | MAE gust |
|---|---|---|---|---|---|
| faible | 230 | +1.18 | 8.46 | +1.23 | 7.91 |
| fort | 80 | -6.55 | 11.04 | +0.80 | 12.27 |
| moyen | 264 | -2.14 | 7.93 | -1.13 | 7.83 |

`gust_model` = ICON brut ; `gust` = carte publiée (corrigée de l'exposition). Les coefficients `GUST_Z_GAIN` et `GUST_SX_GAIN` se règlent à la main sur ce tableau.

## Pluie du jour civil de demain (mm) selon le cumul observé

| pluie_obs | n | biais rain | MAE rain |
|---|---|---|---|
| sec (<0,1 mm) | 214 | +0.19 | 0.20 |
| faible (0,1-2) | 277 | +0.03 | 0.76 |
| modérée (2-10) | 225 | -2.64 | 3.87 |
| forte (>10) | 263 | -10.45 | 18.16 |

Prévision d'un seul membre d'ICON, au pixel de la station : un fort écart sur un jour d'averses est attendu.

## Réglages suggérés (à examiner, pas à appliquer à l'aveugle)

- `AMP_LST_TO_AIR` ≈ **0.84** (régression sur 39 cas de nuit calme et claire ; actuel : voir config).
- `LAPSE_TN (nuits ventées ou couvertes)` ≈ **+1.3 K/km** (950 cas).
- `LAPSE_TX` ≈ **-7.4 K/km** (1118 cas).

À valider sur des jours mis de côté avant de modifier `src/config.py`.
