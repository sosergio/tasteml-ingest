import json
import repositories.tastes as TastesRepo
from datetime import datetime
import urllib.request 
import requests

def readJsonFile(path):
    # this would read the entire file and generate dataframe
    # data_df = pd.read_json("resources/winemag-data-130k-v2.json")
    with open(path) as json_file:  
        return json.load(json_file)

startTime = datetime.now()
updateDb = True

names = readJsonFile("resources/flavours.json")
tastes = []

for tasteName in names[:15]:
    taste = TastesRepo.find_one({'name': tasteName})
    toAdd = False
    if (taste == None):
        requestUrl = "https://server.picular.co/" + urllib.parse.quote(tasteName)
        with urllib.request.urlopen(requestUrl) as url:
            data = json.loads(url.read().decode())
            print("requesting {0} completed after: ".format(requestUrl), (datetime.now() - startTime))
            primary = data['primary']
            secondary = data['secondary']
            taste = {
                'name': tasteName,
                'primary': primary,
                'secondary': secondary,
                'icon': None
            }
            toAdd = True
    if(not hasattr(taste, 'icon')):
        remoteUrl = "https://winefolly-wpengine.netdna-ssl.com/wp-content/uploads/wines/icons/flavors/" + urllib.parse.quote(tasteName) + ".svg"
        localUrl = "resources/icons/" + tasteName + ".svg"
        try:
            with open(remoteUrl) as handle:
                response = requests.get(requestUrl, stream=True)
                if not response.ok:
                    print('no image for ' + tasteName)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
                    taste.icon = localUrl
                    if(not toAdd):
                        TastesRepo.delete_one({'name': tasteName})
                    toAdd = True
        except:
            print('no image for ' + tasteName)
    if(toAdd):
        tastes.append(taste)

# insert in Db
if(updateDb):
    TastesRepo.insertMany(tastes, 100)
    print("insert tags in db completed after: ", (datetime.now() - startTime))
