
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
demo = True
if(demo):
    config.flavoursFilePath = "data/simpleflavours.json"
    config.tastingNotesFilePath = "data/simplereview.json"
    config.sampleCount = 0
    config.numberOfClusters = 2
    config.printDebug = True
    config.updateDb = False
else:
    config.flavoursFilePath = "data/flavours.json"
    config.tastingNotesFilePath = "data/winemag-data-130k-v2.json"
    config.sampleCount = 0
    config.numberOfClusters = 32
    config.printDebug = False
    config.updateDb = True

config.stopWordsFilePath = "data/domainStopWords.json"
config.useStopWords = False


if(runColorTask):
    flavoursRepo = FlavoursRepo(client)
    t = WriteFlavoursWithColorsTask(flavoursRepo, config)
    t.run()

if(runTokenizeTastingNotesTask):
    tastingNotesRepo = TastingNotesRepo(client)
    clusterRepo = ClustersRepo(client)
    t = TokenizeTastingNotes(clusterRepo, tastingNotesRepo, config)
    t.run()
