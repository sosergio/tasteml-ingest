import pymongo
import pprint
import nltk
import json

def insertOne(doc: any, collection: pymongo.collection.Collection):
    pprint.pprint(doc)
    collection.insert_one(doc)

from pymongo import MongoClient
username = "admin"
password = "khCggojq5uP5Wdey"
dbHost = "tasteml-cluster-mc39i"

client = MongoClient(f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('tasteml-db')
collection = db.get_collection('tasting-notes')
for doc in collection.find():
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