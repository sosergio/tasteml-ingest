from pymongo import MongoClient

class TastingNotesRepo:

    def __init__(self, client:MongoClient):
        db = client.get_database('tasteml-db')
        self.collection = db.get_collection('tasting-notes')

    def removeUndefinedProps(self, doc):
        toSave = {}
        for attr, value in doc.items():
            if(value != 0 and attr != "index"):
                toSave[attr] = value
        return toSave

    def add(self, doc: any):    
        self.collection.insert_one(self.removeUndefinedProps(doc))

    def find(self, filter: any):
        return self.collection.find(filter)

    def deleteAll(self):
        self.collection.delete_many({})

    def insertMany(self, data, chunkSize):
        if(chunkSize <= 0):
            chunkSize = 10
        chunk = list()
        counter = 0
        for note in data:
            note = self.removeUndefinedProps(note)
            chunk.append(note)
            counter = counter + 1
            if(chunk.__len__() == chunkSize or counter == data.__len__()):
                self.collection.insert_many(chunk)
                chunk = list()
            