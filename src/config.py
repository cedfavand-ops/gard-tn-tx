"""Paramètres du projet. Tout ce qui est « réglable » est ici."""

# Emprise de calcul (lon0, lat0, lon1, lat1), un peu plus large que le Gard
BBOX = (3.20, 43.40, 4.90, 44.50)
LAT_REF = 44.0

# --- Fenêtres temporelles, en heures depuis 00:00 UTC du jour J (jour de la prévision)
TN_WINDOW = (18, 42)    # J 18:00 -> J+1 18:00
TX_WINDOW = (30, 42)    # J+1 06:00 -> J+1 18:00 (le run ICON-CH1 s'arrête à +33 h : fenêtre parfois tronquée)
NIGHT_WINDOW = (20, 29) # J 20:00 -> J+1 05:00 : heures utilisées pour l'indice d'inversion

# --- Descente d'échelle
ZM_SIGMA_M = 600        # lissage du MNT pour approcher l'orographie du modèle (~1 km)
LAPSE_TN = -0.0065      # K/m, correction d'altitude hors nuit radiative
LAPSE_TX = -0.0070      # K/m, correction d'altitude de jour
HP_SIGMA_M = 1500       # filtre passe-haut de la LST ECOSTRESS (échelle sous-maille du modèle)
AMP_LST_TO_AIR = 0.6    # LST (surface) -> anomalie de T de l'air. À CALIBRER avec des stations.
HP_CLIP = 6.0           # K, écrête les anomalies aberrantes

# --- Indice d'inversion (0 = aucune, 1 = nuit calme et claire)
CLOUD_FULL, CLOUD_ZERO = 20.0, 80.0   # % : <=20 % -> 1 ; >=80 % -> 0
WIND_FULL, WIND_ZERO = 2.0, 5.0       # m/s : <=2 -> 1 ; >=5 -> 0

# --- ECOSTRESS utilisé pour la structure fine
ECOSTRESS_FILES = [   # la première a priorité, la seconde comble les trous
    "data/ecostress/ECO_L2_LSTE_002_LST_doy2023353055606_aid0001.tif",
    "data/ecostress/ECO_L2_LSTE_002_LST_doy2023353055514_aid0001.tif",
]
ECOSTRESS_LABEL = "19/12/2023"

# --- Échelle de couleurs (position 0..1, RGB), proche de celle de la carte Lozère
STOPS = [
    (0.00, (246, 166, 222)), (0.12, (120, 60, 200)), (0.25, (40, 60, 230)),
    (0.38, (40, 190, 240)), (0.50, (60, 220, 120)), (0.62, (220, 230, 50)),
    (0.75, (250, 150, 30)), (0.88, (215, 50, 20)), (1.00, (110, 0, 10)),
]
