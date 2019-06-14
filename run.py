import pymongo
import pprint
import nltk
import json

def insertOne(doc: any, collection: pymongo.collection.Collection):
    pprint.pprint(doc)
    collection.insert_one(doc)


from pymongo import MongoClient
password = "ifhK8pwM6Uhbs8C"
username = "admin"
client = MongoClient(f"mongodb+srv://{username}:{password}@tasteml-db-gndd2.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('tasteml-db')
collection = db.get_collection('tasting-notes')
items = collection.find({})
for doc in items:
    pprint.pprint(doc)

if False:
    count = 0
    with open('dataset/winemag-data-130k-v2.json') as json_file:  
        data = json.load(json_file)
        for note in data:
            if(count  > 10):
                break
            else:
                count= count +1
                insertOne(note, collection)