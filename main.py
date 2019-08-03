from repositories.clusters import ClustersRepo
from repositories.tastes import TastesRepo
from repositories.tastingNotes import TastingNotesRepo
from tasks.setTastes import SetTastesTask
from tasks.tokenizeTastingNotes import TokenizeTastingNotes
from pymongo import MongoClient

runColorTask = False
runTokenizeTastingNotesTask = True

username = "admin"
password = "khCggojq5uP5Wdey"
dbHost = "tasteml-cluster-mc39i"
connection = f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(connection)

if(runColorTask):
    tastesRepo = TastesRepo(client)
    t = SetTastesTask(tastesRepo)
    t.run()

if(runTokenizeTastingNotesTask):
    tastingNotesRepo = TastingNotesRepo(client)
    clusterRepo = ClustersRepo(client)
    t = TokenizeTastingNotes(tastingNotesRepo, clusterRepo)
    t.run()