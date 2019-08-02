from factories.mongoClient import MongoClientFactory
from repositories.clusters import ClustersRepo
from repositories.tastes import TastesRepo
from repositories.tastingNotes import TastingNotesRepo
from tasks.setTastes import SetTastesTask
from tasks.tokenizeTastingNotes import TokenizeTastingNotes

runColorTask = False
runTokenizeTastingNotesTask = False

username = "admin"
password = "khCggojq5uP5Wdey"
dbHost = "tasteml-cluster-mc39i"
client = MongoClientFactory.build(username, password, dbHost)
tastingNotesRepo = TastingNotesRepo(client)
tastesRepo = TastesRepo(client)
clusterRepo = ClustersRepo(client)

if(runColorTask):
    t = SetTastesTask(tastesRepo)
    t.run()

if(runTokenizeTastingNotesTask):
    t = TokenizeTastingNotes(tastingNotesRepo, clusterRepo)
    t.run()