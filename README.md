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
