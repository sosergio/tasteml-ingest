from pymongo import MongoClient

def getCollection():
    username = "admin"
    password = "khCggojq5uP5Wdey"
    dbHost = "tasteml-cluster-mc39i"
    client = MongoClient(f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('tasteml-db')
    return db.get_collection('tastes')

def add(taste: any):    
    getCollection().insert_one(taste)

def find(filter: any):
    return getCollection().find(filter)

def find_one(filter: any):
    return getCollection().find_one(filter)

def deleteAll():
    getCollection().delete_many({})

def delete_one(filter):
    getCollection().delete_one(filter)

def insertMany(data, chunkSize):
    if(chunkSize <= 0):
        chunkSize = 10
    chunk = list()
    counter = 0
    for note in data:
        chunk.append(note)
        counter = counter + 1
        if(chunk.__len__() == chunkSize or counter == data.__len__()):
            getCollection().insert_many(chunk)
            chunk = list()