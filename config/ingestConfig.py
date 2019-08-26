class IngestConfig:
    flavoursFilePath: str
    tastingNotesFilePath: str
    stopWordsFilePath: str
    sampleCount: int = 0
    minWinesPoints: int = 80
    numberOfClusters: int = 32
    useStopWords: bool = False
    updateDb: bool = True
    printDebug: bool = True
    clustering_alg: {'kmean','gmm'} = 'kmean'
