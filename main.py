
from pymongo import MongoClient
from repositories.clusters import ClustersRepo
from repositories.flavours import FlavoursRepo
from repositories.tastingNotes import TastingNotesRepo
from tasks.writeFlavoursWithColors import WriteFlavoursWithColorsTask
from tasks.tokenizeTastingNotes import TokenizeTastingNotes
from config.ingestConfig import IngestConfig


runColorTask = False
runTokenizeTastingNotesTask = True

username = "admin"
password = "khCggojq5uP5Wdey"
dbHost = "tasteml-cluster-mc39i"
connection = f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(connection)

config = IngestConfig()
config.flavoursFilePath = "data/flavours.json"
config.tastingNotesFilePath = "data/winemag-data-130k-v2.json"
config.stopWordsFilePath = "data/domainStopWords.json"

if(runColorTask):
    flavoursRepo = FlavoursRepo(client)
    t = WriteFlavoursWithColorsTask(flavoursRepo, config)
    t.run()

if(runTokenizeTastingNotesTask):
    tastingNotesRepo = TastingNotesRepo(client)
    clusterRepo = ClustersRepo(client)
    t = TokenizeTastingNotes(clusterRepo, tastingNotesRepo, config)
    t.run()
