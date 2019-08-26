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
        self.tokenizeService = TokenizeService(config.printDebug)

    def stopWatchLog(self, str):
        print(f'{str} took {(datetime.now() - self.stopWatchTime)}')
        self.stopWatchTime = datetime.now()

    def printDebug(self, obj):
        if(self.config.printDebug):
            print(obj)

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
        tokens, names = self.tokenizeService.tfidfTokenize(
            data_df['description'], stopWords=stopWords, tokenizer=self.tokenizeService.stemAndTokenizeText)
        self.stopWatchLog(
            f'first pass tokenize, {names.__len__()} tokens found')
        # second pass tokenize
        firstPass_topNames = self.tokenizeService.getTopTokenNames(
            tokens, names, firstPassExcludeTopNamesCount)
        print('firstPass_topNames: ', firstPass_topNames)
        stopWords += list(firstPass_topNames[:firstPassExcludeTopNamesCount])
        tokens, names = self.tokenizeService.tfidfTokenize(
            data_df['description'], stopWords=stopWords, tokenizer=self.tokenizeService.stemAndTokenizeText)
        print('tokens: ', names)
        self.stopWatchLog(
            f'second pass tokenize, {names.__len__()} items found')
        return (tokens, names)

    def tokenizeDataWithVocabulary(self, data_df: DataFrame) -> (any, any):
        flavours_dict = JsonFactory.readJsonFile(self.config.flavoursFilePath)
        flavours_dict_stemmed = self.tokenizeService.lemmaTokenize(flavours_dict)
        tokens, names = self.tokenizeService.tfidfTokenize(
            data_df['description'], vocabulary=flavours_dict_stemmed, tokenizer=self.tokenizeService.stemAndTokenizeText)
        self.stopWatchLog('tokenize with flavours vocabulary')
        return (tokens, flavours_dict)

    def mergeDataWithGMM(self, data_df: DataFrame, tokens: any, names: any, numberOfClusters: int) -> (DataFrame, DataFrame):
        tokens_df = DataFrameFactory.createDataFrame(tokens, names)
        self.printDebug(tokens_df)
        centroids, allDistances = self.tokenizeService.gaussianCluster(
            tokens_df, numberOfClusters)
        cluster_df = DataFrameFactory.createDataFrame(centroids, names)
        self.printDebug(cluster_df)
        colNames = ['to_{0}'.format(s) for s in range(numberOfClusters)]
        allDistances_df = DataFrameFactory.createDataFrame(
            allDistances, colNames)
        self.printDebug(allDistances_df)
        self.stopWatchLog('gmm centroids and all distances')
        # merge dataframes together
        data_withTokens_df = DataFrameFactory.joinDataFrames(
            data_df, tokens_df)
        data_withTokens_andDistanceToCentroids = DataFrameFactory.joinDataFrames(
            data_withTokens_df, allDistances_df)
        self.stopWatchLog('merging dataframes')
        return (data_withTokens_andDistanceToCentroids, cluster_df)
    
    def clusterAndMergeData(self, data_df: DataFrame, tokens: any, names: any, numberOfClusters: int, clusterFn) -> (DataFrame, DataFrame):
        tokens_df = DataFrameFactory.createDataFrame(tokens, names)
        self.printDebug(tokens_df)
        centroids, allDistances = clusterFn(tokens_df, numberOfClusters)
        cluster_df = DataFrameFactory.createDataFrame(centroids, names)
        self.printDebug(cluster_df)
        colNames = ['to_{0}'.format(s) for s in range(numberOfClusters)]
        allDistances_df = DataFrameFactory.createDataFrame(
            allDistances, colNames)
        self.printDebug(allDistances_df)
        self.stopWatchLog(f'{self.config.clustering_alg} centroids and all distances')
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
        # prepare
        data_df = self.prepareData()
        # tokenize
        if(self.config.useStopWords):
            (tokens, names) = self.tokenizeDataWithStopWords(data_df)
        else:
            (tokens, names) = self.tokenizeDataWithVocabulary(data_df)
        # cluster
        clusterFn = self.tokenizeService.kmeanCluster
        if(self.config.clustering_alg == "gmm"):
            clusterFn = self.tokenizeService.gaussianCluster
        (data_withTokens_andDistanceToCentroids, cluster_df) = self.clusterAndMergeData(
            data_df, tokens, names, self.config.numberOfClusters, clusterFn)
        # save
        if(self.config.updateDb):
            self.updateDb(data_withTokens_andDistanceToCentroids, cluster_df)
