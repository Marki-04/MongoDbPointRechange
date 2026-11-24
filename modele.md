# Modèle NoSQL de Point Recharge

> **Remarque :** Le courant de charge n'est pas enregistré, le Raspberry Pi l'utilise en temps réel pour changer l'état du casier. La couleur de la DEL n'est pas enregistrée non plus, car elle se déduit de l'état du casier.

## Collection `stations`
Les casiers sont intégrés dans la station car ils appartiennent à la station et il y en a toujours 8.

```python
station = {
    "_id": "point-recharge-01", 
    "nom": "Point Recharge de la bibliothèque",
    "casiers": [
        {"numero": 1, "etat": "libre"},
        {"numero": 2, "etat": "en_panne"},
        {"numero": 3, "etat": "en_recharge"},
        {"numero": 4, "etat": "libre"},
        {"numero": 5, "etat": "libre"},
        {"numero": 6, "etat": "libre"},
        {"numero": 7, "etat": "libre"},
        {"numero": 8, "etat": "libre"},
    ]
}
```

## Collection `etudiants`

`_id` est le numéro unique de l'étudiant, c'est ce que l'étudiant entre au clavier.

```python
etudiant = {"_id": "1234567", "nom": "Jasmine"}
```

## Collection `depots`
Etudiant.id est une référence vers étudiants, car un étudiant existe sans qu'un dépot existe.
Etudiant.nom est une copie pour simplifier les requêtes, et afficher ex:"déposé par Jasmine"
Casier, qui contient que le numéro qui suffit pour retrouver le casier dans le tableau de la station


```python
depot = {
    "station_id": "point-recharge-01",
    "casier": 3,
    "etudiant":{"id": "1234567", "nom": "Jasmine"},
    "date_depot": datetime(2026,11,24,18,5,tzinfo=timezone.utc),
    "code_hache": "9090",
    "date_retour": None,  # n'a pas encore été retourné
}
```

## Collection `lectures_occupation` TimeSeries
C'est une collection time series parceque le nombre de casiers occupés est une mesure périodique prise toutes les 15 min.
L'id de la station est une référence vers stations car l'historique est illimitée et ne peut pas être intégrée dans le document de la station
Le `_id` est généré car rien autre que l'heure l'identifie.

```python
lectures_occupation = {
    "horodatage": datetime(2026, 11, 24, 18, 15, tzinfo=timezone.utc),
    "station_id": "point-recharge-01",
    "casiers_occupes": 6,
}
```




