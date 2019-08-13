from datetime import datetime
from factories.json import JsonFactory
from repositories.flavours import FlavoursRepo
from services.colors import ColorsService
from config.ingestConfig import IngestConfig


class WriteFlavoursWithColorsTask:
    flavoursRepo: FlavoursRepo
    colorsService: ColorsService
    config: IngestConfig
    
    def __init__(self, flavoursRepo: FlavoursRepo, config: IngestConfig) -> None:
        self.flavoursRepo = flavoursRepo
        self.colorsService = ColorsService()
        self.config = config

    def run(self) -> None:
        startTime = datetime.now()
        updateDb = True

        names = JsonFactory.readJsonFile(self.config.flavoursFilePath)
        flavours = []

        for flavourName in names:
            flavour = self.flavoursRepo.find_one({'name': flavourName})
            if (flavour is None):
                (primary, secondary) = self.colorsService.getColorsFromWord(flavourName)
                flavour = {
                    'name': flavourName,
                    'primary': primary,
                    'secondary': secondary,
                }
                flavours.append(flavour)

        # insert in Db
        if(updateDb):
            self.flavoursRepo.insertMany(flavours, 100)
            print(f'insert flavours in db took: {(datetime.now() - startTime)}')
