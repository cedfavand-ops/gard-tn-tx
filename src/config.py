"""Paramètres du projet. Tout ce qui est « réglable » est ici."""

# Emprise de calcul (lon0, lat0, lon1, lat1), un peu plus large que le Gard
BBOX = (3.20, 43.40, 4.90, 44.50)
LAT_REF = 44.0

# --- Fenêtres temporelles, en heures depuis 00:00 UTC du jour J (jour de la prévision)
TN_WINDOW = (18, 42)    # J 18:00 -> J+1 18:00 UTC
TX_WINDOW = (30, 54)    # J+1 06:00 -> J+2 06:00 UTC (souvent tronquée par l'horizon du run : 33 h, 45 h pour le run de 03 UTC)
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
    (0.76, (250, 150, 30)), (1.00, (205, 15, 20)),
]
# Plages extrêmes de chaque carte : rose uniforme sur [min, min + BAND], rouge uniforme sur [max - BAND, max]
BAND = 0.5   # °C

# Classes discrètes par carte (None = dégradé continu). 20 = 1 rose + 18 intermédiaires + 1 rouge.
N_CLASSES = {"tn": 20, "tx": 20, "gust": 20}
# Placement des bornes des classes intermédiaires : 0 = pas régulier en °C, 1 = classes d'effectif égal
# (le plus de nuances là où il y a le plus de pixels, p. ex. les plaines chaudes). Valeur intermédiaire = compromis.
CLASS_QUANTILE_MIX = 0.5
# Une classe intermédiaire ne peut pas être plus large que ce multiple du pas régulier (évite p. ex. une seule classe 8,9-11,5 °C)
CLASS_MAX_WIDTH_FACTOR = 2.0

# Palette discrète : 1 rose + 18 teintes bien distinctes + 1 rouge vif (utilisée si 20 classes)
CLASS_PINK = (246, 166, 222)
CLASS_PALETTE = [
    (176, 106, 224), (120, 72, 214), (66, 72, 228), (40, 120, 240), (40, 170, 245), (40, 210, 240),
    (40, 215, 190), (50, 210, 140), (80, 205, 90), (140, 215, 60), (195, 228, 50), (235, 232, 50),
    (250, 205, 40), (250, 172, 30), (245, 138, 30), (240, 108, 30), (234, 78, 28), (226, 52, 26),
]
CLASS_RED = (205, 15, 20)

# --- Calibration automatique à partir des stations (voir src/calibration.py)
AUTO_CALIBRATION = False   # False = les cartes utilisent les valeurs ci-dessus. True = elles utilisent data/history/calibration.json
CAL_MIN_N = 30             # nombre minimal de cas (station-jours) pour qu'un réglage puisse bouger
CAL_TEST_FRACTION = 0.3    # part des jours les plus récents mise de côté pour valider
CAL_MIN_GAIN = 0.02        # le nouveau réglage doit réduire l'erreur moyenne d'au moins 2 % sur ces jours
CAL_BOUNDS = {             # bornes de sécurité de chaque paramètre
    "AMP_LST_TO_AIR": (0.2, 1.2),
    "LAPSE_TN": (-0.0100, -0.0030),
    "LAPSE_TX": (-0.0100, -0.0040),
}

# --- Rafales maximales (jour civil de demain, heure de Paris : 00:00 -> 24:00)
GUST_TZ = "Europe/Paris"
GUST_Z_GAIN = 0.15          # +/- 15 % pour une position 100 m au-dessus / au-dessous du relief « vu » par le modèle
GUST_SX_GAIN = 0.25         # +/- 25 % selon l'abri (Sx) par rapport à la direction du vent
GUST_SX_SCALE_DEG = 15.0    # Sx (degrés) à partir duquel l'effet d'abri / d'exposition est maximal
GUST_FACTOR_BOUNDS = (0.6, 1.5)
SX_DISTANCES_M = (300, 600, 1000, 1500, 2200, 3000)   # distances amont examinées pour l'indice d'abri Sx
BAND_GUST = 2.0             # km/h : classes extrêmes uniformes (bas et haut de l'échelle)

# Palette discrète pour les rafales : bleu pâle (calme) -> vert -> jaune -> orange -> rouge -> violet (très fort)
GUST_LOW = (225, 238, 245)
GUST_PALETTE = [
    (170, 225, 240), (120, 210, 235), (70, 195, 225), (60, 185, 180), (70, 190, 130), (110, 200, 90),
    (160, 210, 70), (205, 220, 60), (240, 225, 55), (250, 200, 45), (250, 170, 40), (248, 140, 35),
    (244, 108, 32), (238, 75, 35), (228, 45, 45), (210, 30, 80), (180, 25, 120), (145, 25, 150),
]
GUST_HIGH = (95, 20, 130)

# --- Diagnostic : Tn « nocturne » (21:00 -> 07:00 UTC), archivée à côté de la Tn 18 h -> 18 h UTC
NIGHT_TN_WINDOW = (21, 31)

# --- Correction « mistral » : ICON prévoit des Tn systématiquement trop basses près du Rhône quand le vent est fort
MISTRAL_BIAS_K = 1.25         # K : correction maximale ajoutée à la Tn (vent fort ET proche du Rhône). 0 = désactivée.
MISTRAL_WIND = (3.0, 7.0)     # m/s : vent nocturne moyen où l'effet commence / est maximal
MISTRAL_DIST_KM = 10.0        # distance au Rhône (bord est du département) où l'effet est divisé par e
CAL_BOUNDS["MISTRAL_BIAS_K"] = (0.0, 4.0)
