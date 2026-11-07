"""Les N communes les plus peuplées du Gard, pour l'affichage de leurs noms sur la carte.

Source : geo.api.gouv.fr (noms, populations, centres). Le résultat est mis en cache dans data/communes_gard.json ;
ce fichier peut être modifié à la main (liste de dicts nom / lat / lon / population) : il est alors utilisé tel quel.
Si l'API est indisponible, une liste de secours (valeurs approximatives) est utilisée et non mise en cache."""
import json, os
import requests
from . import config as C

CACHE = "data/communes_gard.json"
URLS = [
    "https://geo.api.gouv.fr/departements/30/communes?fields=nom,population,centre",
    "https://geo.api.gouv.fr/departements/30/communes?fields=nom,population&format=geojson&geometry=centre",
]
# Secours : positions approximatives (centre-ville), populations arrondies, classement incertain au-delà du 10e rang.
FALLBACK = [
    ("Nîmes", 43.8367, 4.3601, 150000), ("Alès", 44.1250, 4.0817, 43000), ("Bagnols-sur-Cèze", 44.1617, 4.6217, 18000),
    ("Beaucaire", 43.8078, 4.6422, 15700), ("Saint-Gilles", 43.6783, 4.4311, 14500), ("Villeneuve-lès-Avignon", 43.9667, 4.7917, 13000),
    ("Vauvert", 43.6942, 4.2778, 11600), ("Pont-Saint-Esprit", 44.2561, 4.6481, 10700), ("Les Angles", 43.9625, 4.7597, 8900),
    ("Aigues-Mortes", 43.5667, 4.1928, 8700), ("Le Grau-du-Roi", 43.5381, 4.1347, 8600), ("Marguerittes", 43.8600, 4.4650, 9000),
    ("Uzès", 44.0120, 4.4195, 8400), ("Rochefort-du-Gard", 43.9867, 4.7000, 8000), ("Laudun-l'Ardoise", 44.1031, 4.6542, 6300),
    ("Bouillargues", 43.8100, 4.4500, 6700), ("Saint-Christol-lès-Alès", 44.0833, 4.0583, 7000), ("Milhaud", 43.7983, 4.3100, 6000),
    ("Sommières", 43.7833, 4.0833, 4700), ("Le Vigan", 43.9919, 3.6256, 3800),
]


def _parse(j):
    items = []
    feats = j.get("features") if isinstance(j, dict) else None
    for it in (feats if feats is not None else j):
        if feats is not None:
            props, geom = it.get("properties", {}), it.get("geometry") or {}
        else:
            props, geom = it, it.get("centre") or {}
        c = geom.get("coordinates")
        if not c or props.get("population") is None:
            continue
        items.append(dict(nom=props["nom"], lat=float(c[1]), lon=float(c[0]), population=int(props["population"])))
    return items


def communes(n=None):
    n = n or C.COMMUNES_N
    if os.path.exists(CACHE):
        return json.load(open(CACHE))[:n]
    for url in URLS:
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            items = sorted(_parse(r.json()), key=lambda d: -d["population"])
            if len(items) >= n:
                items = items[:n]
                os.makedirs("data", exist_ok=True)
                json.dump(items, open(CACHE, "w"), ensure_ascii=False, indent=1)
                print(f"[COMMUNES] {n} communes récupérées (plus peuplée : {items[0]['nom']})", flush=True)
                return items
        except Exception as e:
            print(f"[COMMUNES] {url} indisponible ({type(e).__name__})", flush=True)
    print("[COMMUNES] liste de secours utilisée", flush=True)
    return [dict(nom=a, lat=b, lon=c, population=d) for a, b, c, d in FALLBACK][:n]


def write_communes(out):
    items = communes()
    json.dump([dict(n=d["nom"], lat=round(d["lat"], 4), lon=round(d["lon"], 4), p=d["population"]) for d in items],
              open(f"{out}/communes.json", "w"), ensure_ascii=False)
