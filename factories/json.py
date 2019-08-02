import json

class JsonFactory:

    @staticmethod    
    def readJsonFile(path):
        # this would read the entire file and generate dataframe
        # data_df = pd.read_json("resources/winemag-data-130k-v2.json")
        with open(path) as json_file:  
            return json.load(json_file)
