from pymongo import MongoClient

class TastesRepo:

    def __init__(self, client):
        db = client.get_database('tasteml-db')
        collection = db.get_collection('tastes')
        self.collection = collection

    def add(self, taste: any):    
        self.collection.insert_one(taste)

    def find(self, filter: any):
        return self.collection.find(filter)

    def find_one(self, filter: any):
        return self.collection.find_one(filter)

    def deleteAll(self):
        self.collection.delete_many({})

    def delete_one(self, filter):
        self.collection.delete_one(filter)

    def insertMany(self, data, chunkSize):
        if(chunkSize <= 0):
            chunkSize = 10
        chunk = list()
        counter = 0
        for note in data:
            chunk.append(note)
            counter = counter + 1
            if(chunk.__len__() == chunkSize or counter == data.__len__()):
                self.collection.insert_many(chunk)
                chunk = list()