# Gard – prévision de Tn et Tx du lendemain (150 m)

Cartes expérimentales publiées sur GitHub Pages, recalculées chaque jour par GitHub Actions.

- **Tn** : minimum ICON-CH1-EPS (run de contrôle) ramené à la maille par une correction d'altitude (MNT Copernicus GLO-30).
  Lors des nuits radiatives (indice d'inversion proche de 1, fondé sur la nébulosité et le vent nocturnes),
  la correction d'altitude est remplacée par la structure fine d'une thermographie **ECOSTRESS** (anomalie de LST filtrée passe-haut,
  facteur `AMP_LST_TO_AIR`). Mélange continu entre les deux selon l'indice.
- **Tx** : maximum ICON-CH1 corrigé du relief (pas d'ECOSTRESS). Fenêtres (UTC) : Tn de J 18:00 à J+1 18:00 ; Tx de J+1 06:00 à J+2 06:00,
  souvent tronquée car le run ICON-CH1 ne va qu'à +33 h (indiqué sur la page).
- Page : valeurs au survol, isolignes fines tous les 1 °C et épaisses tous les 5 °C, fond OpenStreetMap ou Plan IGN (sans clé API).
- Pas de pas 70 m : `--res 70` (calcul plus lourd, mêmes scripts).

## Mise en route
1. Créez un dépôt **public** GitHub et poussez ce dossier (les deux `.tif` ECOSTRESS pèsent ~20 Mo, c'est accepté).
2. *Settings → Pages → Build and deployment → Source : **GitHub Actions***.
3. *Actions → « Prévision Tn/Tx Gard » → Run workflow*. Au premier lancement, MNT et masque sont téléchargés puis mis en cache.
4. La page est ensuite à `https://<utilisateur>.github.io/<dépôt>/`. Le calcul est relancé tous les jours à 14:20 UTC.

## Test local sans réseau
```
pip install numpy scipy Pillow tifffile matplotlib
python -m src.run --demo --out site && python -m http.server -d site
```
`--demo` utilise un MNT et des champs ICON synthétiques (seul ECOSTRESS est réel) : la carte n'a aucune valeur météo.
`--force-inversion 1` force la nuit radiative pour visualiser l'effet maximal.

## À savoir
- `src/icon.py › fetch_icon` n'a **pas pu être testé** sur le vrai service. Si vous avez déjà une lecture d'ICON-CH1 qui marche
  (projet Lozère), remplacez cette fonction : elle doit renvoyer un `IconData`.
- OGD ne garde que ~24 h de runs : un jour sans exécution est perdu.
- `AMP_LST_TO_AIR` (0,6) et la formule de l'indice d'inversion (`config.py`) sont des choix de départ à caler sur des stations.
  Le Rhône et les étangs, chauds la nuit, ressortent fortement dans l'anomalie LST.
- La scène ECOSTRESS du 19/12/2023 est une seule situation ; ajoutez d'autres passages nocturnes de ciel clair et moyennez-les dans `static.py`.

## Sources et licences
MeteoSwiss Open Government Data (ICON-CH1-EPS) · ECOSTRESS L2 LSTE (NASA LP DAAC) · Copernicus DEM GLO-30 · contour des départements : geo.api.gouv.fr · fond de carte © OpenStreetMap, © CARTO.

## Vérification avec les stations Météo-France (Gard)
Chaque jour, le workflow : (1) télécharge les données horaires ouvertes du département 30 et en tire la liste des stations actives et les Tn/Tx
observées des jours passés ; (2) archive les prévisions aux points de stations (`data/history/forecasts.csv`) ; (3) écrit `data/history/report.md`
(biais et erreur moyenne par situation ciel/vent, par altitude, et réglages suggérés pour `AMP_LST_TO_AIR` et les gradients d'altitude) ;
(4) enregistre l'historique dans le dépôt. Rien n'est archivé en mode `--demo`. Les étapes 1, 3 et 4 n'empêchent jamais la publication de la page.

## Calibration automatique (inactive par défaut)
Chaque lundi (et à chaque lancement manuel), `src/calibration.py` réajuste `AMP_LST_TO_AIR`, `LAPSE_TN` et `LAPSE_TX` à partir de l'historique des stations :
régression ramenée vers les valeurs de `config.py` (poids équivalent à `CAL_MIN_N` cas), bornes `CAL_BOUNDS`, et validation sur les derniers jours mis de côté
(le réglage n'est retenu que s'il réduit l'erreur d'au moins `CAL_MIN_GAIN`). Le résultat est écrit dans `data/history/calibration.json` (journal : `calibration_log.csv`).
Les cartes n'utilisent ce fichier que si `AUTO_CALIBRATION = True` dans `src/config.py` ; pour revenir en arrière, remettre `False`.

## Carte des rafales (expérimentale)
Rafale maximale (`VMAX_10M` d'ICON-CH1) sur le jour civil de demain, **00:00 → 24:00 heure de Paris** (fuseau réglable : `GUST_TZ`), ramenée à la maille par un facteur d'exposition :
position par rapport au relief « vu » par le modèle (`GUST_Z_GAIN`) et indice d'abri Sx dans la direction du vent au moment du maximum (`GUST_SX_GAIN`, `data/sx_<res>.npz` en cache).
Le facteur est normalisé à l'échelle du modèle (la moyenne sur ~1 km reste celle d'ICON). Le run principal s'arrête à +33 h ; la fin de la journée est complétée avec le run de 03 UTC (+45 h) quand il existe.
Les rafales observées (colonne FXI Météo-France) sont archivées et comparées dans `report.md` ; leurs coefficients ne sont pas calibrés automatiquement.

## Correction « mistral » (Tn)
ICON prévoit des Tn systématiquement trop basses près du Rhône quand le vent est fort. La Tn reçoit donc `+ MISTRAL_BIAS_K × s(vent) × proximité` :
`s` croît de 0 à 1 entre 3 et 7 m/s de vent nocturne moyen (`MISTRAL_WIND`), la proximité vaut exp(−d / `MISTRAL_DIST_KM`) avec d = distance au bord est du département (le Rhône).
`MISTRAL_BIAS_K = 1.25` K au départ ; la calibration automatique (inactive) l'ajuste ensuite sur les stations (bornes 0 à 4 K). Mettre 0 pour désactiver.

## Pluie et nuages
- **Pluie** : cumul `TOT_PREC` d'ICON-CH1 (membre de contrôle) sur le jour civil de demain, 00:00 → 24:00 heure de Paris. Run principal jusqu'à son horizon,
  puis run de 03 UTC (+45 h) pour la fin de journée. Seuils fixes (0,1 mm à ≥ 200 mm), du bleu pâle au violet, transparent sous 0,1 mm (`RAIN_EDGES`, `RAIN_PALETTE`).
  Interpolation de la valeur du modèle, sans correction de relief à 150 m. Archivée aux stations et comparée au cumul observé (`RR1`).
- **Nuages** : composite des couvertures `CLCL` (bas, rouge), `CLCM` (moyens, vert), `CLCH` (élevés, bleu) à 9 h, 12 h et 15 h heure de Paris (`CLOUD_HOURS_LOCAL`).
  Teinte = proportions des trois étages, opacité = couverture la plus forte. Au survol : pourcentage de chaque étage.

## Cuvettes froides (Tn, nuits radiatives)
En plus de la structure ECOSTRESS, un terme physique `INV_DZ_GAIN` (K/m) × (altitude − altitude lissée sur `INV_ZM_SIGMA_M`) est ajouté au prorata de l'indice d'inversion :
creux plus froids, replats surélevés plus doux, même là où ECOSTRESS n'a pas de donnée. Formule de la Tn : `(1 − inv) × (ICON + gradient d'altitude) + inv × (ICON + AMP × ECOSTRESS + INV_DZ_GAIN × creux)`.
`INV_DZ_GAIN` est aussi calibrable sur les stations (bornes 0 à 0,15 K/m).

## Stations supplémentaires et observations manuelles
- `data/stations_extra.csv` (id, name, lat, lon, alti) : stations hors Météo-France dont on veut archiver la prévision (La Lèque y figure).
- `data/obs_manual.csv` (jour, id, tn_obs, tx_obs [, gust_obs, rain_obs]) : observations saisies à la main. `jour` = jour **observé** (matin pour la Tn, après-midi pour la Tx) ;
  la prévision correspondante est celle émise la veille. Elles s'ajoutent aux observations Météo-France pour le rapport et la calibration.
- La structure ECOSTRESS est désormais recalculée à chaque exécution (le cache ne garde que MNT et masque) : modifier `HP_SIGMA_M`, `HP_CLIP` ou `AMP_LST_TO_AIR` agit tout de suite.
