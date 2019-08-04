from pymongo import MongoClient


class ClustersRepo:

    def __init__(self, client: MongoClient):
        db = client.get_database('tasteml-db')
        self.collection = db.get_collection('clusters')

    def add(self, doc: any):
        self.collection.insert_one(doc)

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
            chunk.append(note)
            counter = counter + 1
            if(chunk.__len__() == chunkSize or counter == data.__len__()):
                self.collection.insert_many(chunk)
                chunk = list()
