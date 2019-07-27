import json
import repositories.tastes as TastesRepo
from datetime import datetime
import urllib.request 

def readJsonFile(path):
    # this would read the entire file and generate dataframe
    # data_df = pd.read_json("resources/winemag-data-130k-v2.json")
    with open(path) as json_file:  
        return json.load(json_file)

startTime = datetime.now()
updateDb = True

names = readJsonFile("resources/flavours.json")
tastes = []

for taste in names:
    if (TastesRepo.find({'name': taste}).count() == 0):
        requestUrl = "https://server.picular.co/" + urllib.parse.quote(taste)
        with urllib.request.urlopen(requestUrl) as url:
            data = json.loads(url.read().decode())
            print("requesting {0} completed after: ".format(requestUrl), (datetime.now() - startTime))
            primary = data['primary']
            secondary = data['secondary']
            tastes.append({
                'name': taste,
                'primary': primary,
                'secondary': secondary
            })

# insert in Db
if(updateDb):
    TastesRepo.insertMany(tastes, 100)
    print("insert tags in db completed after: ", (datetime.now() - startTime))
