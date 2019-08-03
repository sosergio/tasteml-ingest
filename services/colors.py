from datetime import datetime
import urllib.request 
import json

class ColorsService:
    
    def getColorsFromWord(self, word: str) -> (str,str):
        startTime = datetime.now()
        if (word != None):
            requestUrl = "https://server.picular.co/" + urllib.parse.quote(word)
            with urllib.request.urlopen(requestUrl) as url:
                data = json.loads(url.read().decode())
                print("requesting {0} completed after: ".format(requestUrl), (datetime.now() - startTime))
                primary = data['primary']
                secondary = data['secondary']
                return (primary, secondary)