from pymongo import MongoClient
import pprint

def getCollection():
    username = "admin"
    password = "khCggojq5uP5Wdey"
    dbHost = "tasteml-cluster-mc39i"
    client = MongoClient(f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('tasteml-db')
    return db.get_collection('tasting-notes')

def add(doc: any):
    toSave = {}
    for attr, value in doc.items():
        if(value != 0 and attr != "index"):
            toSave[attr] = value
    getCollection().insert_one(toSave)

def find(filter: any):
    getCollection().find(filter)

def deleteAll():
    getCollection().delete_many({})

def insertMany(data):
    for note in data:
        add(note)