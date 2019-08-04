from datetime import datetime
from factories.json import JsonFactory
from repositories.tastes import TastesRepo
from services.colors import ColorsService
from config.ingestConfig import IngestConfig


class SetTastesTask:
    tasteRepo: TastesRepo
    colorsService: ColorsService
    config: IngestConfig
    
    def __init__(self, tasteRepo: TastesRepo, config: IngestConfig) -> None:
        self.tasteRepo = tasteRepo
        self.colorsService = ColorsService()
        self.config = config

    def run(self) -> None:
        startTime = datetime.now()
        updateDb = True

        names = JsonFactory.readJsonFile(self.config.flavoursFilePath)
        tastes = []

        for tasteName in names:
            taste = self.tasteRepo.find_one({'name': tasteName})
            if (taste is None):
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
            print(f'insert tags in db took: {(datetime.now() - startTime)}')
