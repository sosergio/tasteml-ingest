from pymongo import MongoClient

def getCollection():
    username = "admin"
    password = "khCggojq5uP5Wdey"
    dbHost = "tasteml-cluster-mc39i"
    client = MongoClient(f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('tasteml-db')
    return db.get_collection('tastes')

def createTag(words):
    return {"all": words}

def add(words: any):    
    getCollection().insert_one(createTag(words))

def find(filter: any):
    getCollection().find(filter)

def deleteAll():
    getCollection().delete_many({})