import pymongo
import pprint

from pymongo import MongoClient
password = "ifhK8pwM6Uhbs8C"
username = "admin"
client = MongoClient(f"mongodb+srv://{username}:{password}@tasteml-db-gndd2.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('tasteml-db')
collection = db.get_collection('tasting-notes')
item = collection.find_one()
pprint.pprint(item)