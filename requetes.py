from pymongo import MongoClient
from datetime import datetime, timezone

import config

client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000, tz_aware=True)
db = client[config.MONGODB_BASE]

STATION = "point-recharge-01"
minuit = datetime.now(config.FUSEAU_LOCAL).replace(hour=0, minute=0, second=0, microsecond=0)

# Q1
oublies = db.depots.find(
    {
        "station_id": STATION,
        "date_depot": {"$lt": minuit},
        "date_retour": None,
    },
    {
        "id":1,
        "casier": 1,
        "etudiant.nom": 1,
        "date_depot": 1, 
    }).sort("date_depot", 1)
print("Télephones oubliés:")
for o in oublies:
    date = o["date_depot"].astimezone(config.FUSEAU_LOCAL).strftime("%Y-%m-%d %H:%M")
    print(f"Casier:{o['casier']}-{o['etudiant']['nom']} | Déposé le {date}")


# Q2
# Fonction pour embarrer et mettre en charge  un téléphone. 
# Prends en paramètre, le numéro de l'étudiant(validé avec ce que contient la BD), Le numéro de casier (validé avec ce que contient la BD), code (validé que ca soit 4 chiffres)
def enregistrer_depot(numero_etudiant: str, numero_casier: int, code:str)->None:
    etudiant= db.etudiants.find_one({"_id": numero_etudiant})
    if etudiant is None:
        print("L'étudiant n'existe pas dans la BD")
        return
    if len(code) != 4 or not code.isdigit():
        print("Le code doit être écrit avec 4 chiffres seulement")
        return
    station = db.stations.find_one(
        {
            "_id":STATION, 
            "casiers.numero":numero_casier
        },
        {
            "_id":0,
            "casiers.$":1
        })
    
    if station is None:
        print("Le casier entré n'existe pas")
        return
    if station["casiers"][0]["etat"] != "libre":
        print("Le casier choisi est présentement occupé")
        return

    db.depots.insert_one({
        "station_id": STATION,
        "casier": numero_casier,
        "code_hache": code,
        "etudiant": {"id":etudiant["_id"], "nom": etudiant["nom"]},
        "date_depot":datetime.now(timezone.utc),
        "date_retour": None,
    })
    db.stations.update_one({"_id": STATION, "casiers.numero":numero_casier},
                           {"$set": {"casiers.$.etat": "en_charge"}},
                           )
    print("Le casier à bien été barré et votre téléphone a été mis en charge!")

# Tests d'insertion
enregistrer_depot("1234567", 1, "4321")
enregistrer_depot("1234567", 1, "4321")
enregistrer_depot("0000000", 4, "1234")
enregistrer_depot("9876543", 6, "12")

    
    