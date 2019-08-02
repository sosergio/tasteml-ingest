from factories.json import JsonFactory
from repositories.tastes import TastesRepo
from datetime import datetime
import urllib.request 
import requests
import json

class SetTastesTask:
    tasteRepo: TastesRepo
    def __init__(self, tasteRepo: TastesRepo) -> None:
        self.tasteRepo = tasteRepo

    def run(self) -> None:
        startTime = datetime.now()
        updateDb = True

        names = JsonFactory.readJsonFile("resources/flavours.json")
        tastes = []

        for tasteName in names[:15]:
            taste = self.tasteRepo.find_one({'name': tasteName})
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
                                self.tasteRepo.delete_one({'name': tasteName})
                            toAdd = True
                except:
                    print('no image for ' + tasteName)
            if(toAdd):
                tastes.append(taste)

        # insert in Db
        if(updateDb):
            self.tasteRepo.insertMany(tastes, 100)
            print("insert tags in db completed after: ", (datetime.now() - startTime))
