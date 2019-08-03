from factories.json import JsonFactory
from repositories.tastes import TastesRepo
from services.colors import ColorsService
from datetime import datetime
import urllib.request 
import json

class SetTastesTask:
    tasteRepo: TastesRepo
    colorsService: ColorsService

    def __init__(self, tasteRepo: TastesRepo) -> None:
        self.tasteRepo = tasteRepo
        self.colorsService = ColorsService()

    def run(self) -> None:
        startTime = datetime.now()
        updateDb = True

        names = JsonFactory.readJsonFile("resources/flavours.json")
        tastes = []

        for tasteName in names:
            taste = self.tasteRepo.find_one({'name': tasteName})
            if (taste == None):
                (primary, secondary) = self.colorsService.getColorsFromWord(tasteName)
                taste = {
                    'name': tasteName,
                    'primary': primary,
                    'secondary': secondary,
                }
                tastes.append(taste)

        # insert in Db
        if(updateDb):
            self.tasteRepo.insertMany(tastes, 100)
            print("insert tags in db took: ", (datetime.now() - startTime))
