from pymongo import MongoClient

def getCollection():
    username = "admin"
    password = "khCggojq5uP5Wdey"
    dbHost = "tasteml-cluster-mc39i"
    client = MongoClient(f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('tasteml-db')
    return db.get_collection('tasting-notes')

def removeUndefinedProps(doc):
    toSave = {}
    for attr, value in doc.items():
        if(value != 0 and attr != "index"):
            toSave[attr] = value
    return toSave

def add(doc: any):    
    getCollection().insert_one(removeUndefinedProps(doc))

def find(filter: any):
    return getCollection().find(filter)

def deleteAll():
    getCollection().delete_many({})

def insertMany(data, chunkSize):
    if(chunkSize <= 0):
        chunkSize = 10
    chunk = list()
    counter = 0
    for note in data:
        note = removeUndefinedProps(note)
        chunk.append(note)
        counter = counter + 1
        if(chunk.__len__() == chunkSize or counter == data.__len__()):
            getCollection().insert_many(chunk)
            chunk = list()