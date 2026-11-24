from datetime import datetime, timedelta, timezone
from random import randint

from pymongo import MongoClient

import config

client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000, tz_aware=True)
db = client[config.MONGODB_BASE]

# Supprimer TOUTES* les collections existantes
for nom in db.list_collection_names():
    if not nom.startswith("system."):
        db.drop_collection(nom)

db.create_collection(
    "lectures_occupation",
    timeseries={
        "timeField": "horodatage",
        "metaField": "station_id",
        "granularity": "minutes",
    }
)

STATION = "point-recharge-01"
maintenant = datetime.now(timezone.utc)

etats = {1: "libre", 2: "en_panne", 3: "en_charge", 4: "libre", 5: "charge", 6: "libre", 7: "libre", 8: "charge"}

db.stations.insert_one({
    "_id": STATION, 
    "nom": "Point Recharge de la bibliothèque",
    "casiers": [{"numero":n, "etat":etat} for n, etat in etats.items()]
    }
)

jasmine, sophia, shanys = [
    {"_id": "1234567", "nom": "Jasmine"},
    {"_id": "9876543", "nom": "Sophia"},
    {"_id": "3216549", "nom": "Shanys"},
]
db.etudiants.insert_many([jasmine, sophia, shanys])

def depot(etudiant, casier, date_depot, code, date_retour=None):
    return {
        "station_id": STATION,
        "casier": casier,
        "code_hache": code,
        "etudiant": {"id":etudiant["_id"], "nom": etudiant["nom"]},
        "date_depot":date_depot,
        "date_retour": date_retour,
    }
hier = maintenant - timedelta(days=1)

db.depots.insert_many([
    depot(sophia, 2, maintenant - timedelta(minutes=50), "1111"),
    depot(jasmine, 3, maintenant-timedelta(minutes=20), "2222"),
    depot(sophia, 5, hier.replace(hour=0) + timedelta(hours=1), "3333"),
    depot(shanys, 8, hier - timedelta(hours=2), "4444"),
    depot(jasmine, 4, hier - timedelta(hours=5), "5555", date_retour=hier - timedelta(hours=3))
])

occupations = [
    {
        "horodatage": maintenant - timedelta(minutes=15 *i),
        "station_id": STATION,
        "casiers_occupes": 4 if i== 0 else randint(1, 8)
    }
    for i in range (16)
]
db.lectures_occupation.insert_many(occupations)

for nom in db.list_collection_names():
    if not nom.startswith("system."):
        print(f"{nom} : {db[nom].count_documents({})}")

client.close()