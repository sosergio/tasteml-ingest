import pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction import text
from nltk.corpus import stopwords
from datetime import datetime
from repositories.tastingNotes import TastingNotesRepo
from repositories.clusters import ClustersRepo
from factories.json import JsonFactory
from factories.dataFrame import DataFrameFactory
from services.tokenize import TokenizeService
from config.ingestConfig import IngestConfig

class TokenizeTastingNotes:
    stopWatchTime: datetime
    config: IngestConfig

    def __init__(self, clustersRepo: ClustersRepo, tastingNotesRepo: TastingNotesRepo, config: IngestConfig):
        self.tastingNotesRepo = tastingNotesRepo
        self.clustersRepo = clustersRepo
        self.config = config
        self.stopWatchTime = datetime.now()

    def stopWatchLog(self, str):
        print(f'{str} took {(datetime.now() - self.stopWatchTime)}')
        self.stopWatchTime = datetime.now()

    def prepareData(self) -> DataFrame:
        sampleCount = self.config.sampleCount
        data = JsonFactory.readJsonFile(self.config.tastingNotesFilePath)
        # reduce the list to wines that have more points than the ones specified
        points = self.config.minWinesPoints
        data_topQuality = list(
            filter(lambda x: int(x['points']) > points, data))
        print('items with top quality', data_topQuality.__len__())
        # reduce to a sampling set, used during development
        if(sampleCount > 0):
            data_sample = data_topQuality[:sampleCount]
            print('first {0} items sampled'.format(sampleCount))
        else:
            data_sample = data_topQuality
        data_df = DataFrameFactory.generateDataFrame(data_sample)
        # remove rows wich have nulls
        data_df.dropna()
        # transform points column from string to numbers
        data_df['points'] = data_df['points'].apply(pd.to_numeric)
        # attach a column for quality/price ratio
        data_df['ratio'] = data_df.apply(
            lambda row: (row.points / row.price), axis=1)
        self.stopWatchLog('preapare data')
        return data_df

    def tokenizeDataWithStopWords(self, data_df: DataFrame) -> (any, any):
        firstPassExcludeTopNamesCount = 10
        # define all stop-words
        domainStopWords = list(JsonFactory.readJsonFile(
            self.config.stopWordsFilePath))
        __sw = list(stopwords.words('english'))
        stopWords = domainStopWords + __sw + list(text.ENGLISH_STOP_WORDS)
        # first pass tokenize
        tokens, names = TokenizeService.tfidfTokenize(
            data_df['description'], stopWords=stopWords)
        self.stopWatchLog(
            f'first pass tokenize, {names.__len__()} items found')
        # second pass tokenize
        firstPass_topNames = TokenizeService.getTopTokenNames(
            tokens, names, firstPassExcludeTopNamesCount)
        print('firstPass_topNames: ', firstPass_topNames)
        stopWords += list(firstPass_topNames[:firstPassExcludeTopNamesCount])
        tokens, names = TokenizeService.tfidfTokenize(
            data_df['description'], stopWords, None)
        names = TokenizeService.getTopTokenNames(tokens, names, 200)
        print('keeping only first 200 top names: ', names)
        tokens, names = TokenizeService.tfidfTokenize(
            data_df['description'], None, names)
        self.stopWatchLog(
            f'first pass tokenize, {names.__len__()} items found')
        return (tokens, names)

    def tokenizeDataWithVocabulary(self, data_df: DataFrame) -> (any, any):
        flavours_dict = JsonFactory.readJsonFile(self.config.flavoursFilePath)
        tokens, names = TokenizeService.tfidfTokenize(
            data_df['description'], vocabulary=flavours_dict)
        self.stopWatchLog('tokenize with flavours vocabulary')
        return (tokens, names)

    def mergeDataWithKMeans(self, data_df: DataFrame, tokens: any, names: any, numberOfClusters: int) -> (DataFrame, DataFrame):
        tokens_df = DataFrameFactory.createDataFrame(tokens, names)
        centroids, allDistances = TokenizeService.kmeanCluster(
            tokens_df, numberOfClusters)
        cluster_df = DataFrameFactory.createDataFrame(centroids, names)
        colNames = ['to_{0}'.format(s) for s in range(numberOfClusters)]
        allDistances_df = DataFrameFactory.createDataFrame(
            allDistances, colNames)
        self.stopWatchLog('kmean centroids and all distances')
        # merge dataframes together
        data_withTokens_df = DataFrameFactory.joinDataFrames(
            data_df, tokens_df)
        data_withTokens_andDistanceToCentroids = DataFrameFactory.joinDataFrames(
            data_withTokens_df, allDistances_df)
        self.stopWatchLog('merging dataframes')
        return (data_withTokens_andDistanceToCentroids, cluster_df)

    def updateDb(self, data_withTokens_andDistanceToCentroids: DataFrame, cluster_df: DataFrame):
        insertManyInChunksOf = 250
        cluster_list = DataFrameFactory.convertDataFrameToList(cluster_df)
        data_withTokens_andDistanceToCentroids_list = DataFrameFactory.convertDataFrameToList(
            data_withTokens_andDistanceToCentroids)
        self.stopWatchLog('merging dataframes')
        self.tastingNotesRepo.deleteAll()
        self.tastingNotesRepo.insertMany(
            data_withTokens_andDistanceToCentroids_list, insertManyInChunksOf)
        self.stopWatchLog('insert tasting notes in db')
        self.clustersRepo.deleteAll()
        self.clustersRepo.insertMany(cluster_list, insertManyInChunksOf)
        self.stopWatchLog('insert clusters in db')

    def run(self):
        self.stopWatchTime = datetime.now()
        data_df = self.prepareData()
        if(self.config.useStopWords):
            (tokens, names) = self.tokenizeDataWithStopWords(data_df)
        else:
            (tokens, names) = self.tokenizeDataWithVocabulary(data_df)
        (data_withTokens_andDistanceToCentroids, cluster_df) = self.mergeDataWithKMeans(
            data_df, tokens, names, self.config.numberOfClusters)
        if(self.config.updateDb):
            self.updateDb(data_withTokens_andDistanceToCentroids, cluster_df)
