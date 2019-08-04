class IngestConfig:
    flavoursFilePath: str
    tastingNotesFilePath: str
    stopWordsFilePath: str
    sampleCount: int = 0
    minWinesPoints: int = 80
    numberOfClusters: int = 32
    useStopWords: bool = False
    updateDb: bool = True
