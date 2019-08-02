import nltk
import json
from factories.mongodb import MongoDbConnection
from repositories.tastingNotes import TastingNotesRepo
import repositories.tastes as TastesRepo
import repositories.clusters as ClustersRepo
import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime
from nltk.stem.porter import PorterStemmer
from factories.json import JsonFactory
from factories.dataFrame import DataFrameFactory

# returns a new list of wines that have more points than the one specified
def filterWithQuality(points:int, data:any):
        return list(filter(lambda x: int(x["points"]) > points, data))

# taekes away punctuation, capitalization, and generic stopwords
def getStopWords():
    domainStopWords = list(["tannins","flavor","flavour","wine","hints","notes","aromas","character","bit","palate","flavors","drink","finish","fruit","offers","style","hint","drinkable",
        "imported", "spiciness", "400", "beatifully", "sierra", "harmonious", "feet", "grown", "accented", "range", "vines", "grained", "classic", "tannic",
        "excess", "essential", "estate", "estates", "etienne", "excels", "everyday", "example", "exceptional", "excellent", "exceedingly", "zippy", "erath",
        "equal", "elevation", "emerge", "emerges", "emphasis", "end", "ending", "ends", "enduring", "energetic", "spiciness", "fine", "exudes",
        "extracted", "fair", "extract", "fairly", "farmers", "falls", "fare", "farmed",
        "fascinating", "fat", "favors", "features", "feed", "feel", "feeling", "extends",
        "expression", "extended",  "enjoyable", "enjoyed" ,"enough",
        "enriched", "ensures", "enticing", "entry", "envelopes", "even",
        "extend", "everything", "except", "exciting", "expect", "creates", "finds", "finesse", "finessed", "finest", "finished", "finishes", "finishing", 
        "fills", "first", "fist", "five", "create", "flagship", "find", "field", "filled", "flint", "elegance", "elegant", "elegantly", "element", "elements", "elevated", "enhanced", "enjoy"
    ])
    __sw = list(stopwords.words("english"))
    return domainStopWords + __sw + list(text.ENGLISH_STOP_WORDS)

# returns a new DataFrame where every row is the TF-IDF tokenization of the collection passed in, with stopwords
# consider Stemming: reducing similar words to a base stem) and
# consiedr Word Categorizing: analyze sentences to categorize words like adjectives, nouns, ...
def tokenize(coll:any, stopWords:any, vocabulary:any):
    if(stopWords):
        vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=stopWords)
    else:
        vectorizer = TfidfVectorizer(ngram_range=(1,1), vocabulary=vocabulary)
    tokens = vectorizer.fit_transform(coll).toarray()
    names = vectorizer.get_feature_names()
    print("names found", names.__len__())
    return tokens, names

def getTopTokenNames(tokens, names, limit):
    array = np.array(names)
    sorting = np.argsort(tokens).flatten()[::-1]
    return array[sorting][:limit]

def getKMean(dataFrame, numberOfClusters):
    kmeans = KMeans(n_clusters=numberOfClusters)
    alldistances = kmeans.fit_transform(dataFrame)
    np.round_(alldistances,3,alldistances)
    centroids = kmeans.cluster_centers_
    return centroids, alldistances

class TokenizeTastingNotes:
        
    def __init__(self, tastingNotesRepo:TastingNotesRepo, clustersRepo:ClustersRepo):
        self.tastingNotesRepo = tastingNotesRepo
        self.clustersRepo = clustersRepo

    def run(self):
        startTime = datetime.now()

        sampleCount = 5000
        firstPassExcludeTopNamesCount = 10
        numberOfClusters = 15
        insertManyInChunksOf = 250
        updateDb = True
        useStopWords = False

        data = JsonFactory.readJsonFile("resources/winemag-data-130k-v2.json")
        flavours_dict = JsonFactory.readJsonFile("resources/flavours.json")
        data_topQuality = filterWithQuality(80, data)
        print("items with top quality", data_topQuality.__len__())
        data_sample = data_topQuality[:sampleCount]
        data_df = DataFrameFactory.generateDataFrame(data_sample)
        # remove rows wich have nulls
        data_df.dropna()
        # transform points column from string to numbers
        data_df["points"] = data_df["points"].apply(pd.to_numeric)
        # attach a column for quality/price ratio
        data_df['ratio'] = data_df.apply(lambda row: row.points/row.price, axis=1)
        print("load file completed after: ", (datetime.now() - startTime))

        # first pass tokenize
        if(useStopWords):
            stopWords = getStopWords()
            tokens, names = tokenize(data_df["description"], stopWords, None)
        else:
            tokens, names = tokenize(data_df["description"], None, flavours_dict)
        print("first pass tokenize completed after: ", (datetime.now() - startTime))

        # second pass tokenize
        if(useStopWords):
            firstPass_topNames = getTopTokenNames(tokens, names, firstPassExcludeTopNamesCount)
            print("firstPass_topNames: ", firstPass_topNames)
            stopWords = stopWords + list(firstPass_topNames[:firstPassExcludeTopNamesCount])
            tokens, names = tokenize(data_df["description"], stopWords, None)
            names = getTopTokenNames(tokens, names, 200)
            print("keeping only first 200 top names: ", names)
            tokens, names = tokenize(data_df["description"], None, names)
            print("second pass tokenize completed after: ", (datetime.now() - startTime))

        tokens_df = DataFrameFactory.createDataFrame(tokens, names)
        print("dataframe completed after: ", (datetime.now() - startTime))

        # calculate the kmean centroids and all distances (item to centroids)
        centroids, allDistances = getKMean(tokens_df, numberOfClusters)
        cluster_df = DataFrameFactory.createDataFrame(centroids, names)
        cluster_list = DataFrameFactory.convertDataFrameToList(cluster_df)
        colNames = ['to_{0}'.format(s) for s in range(numberOfClusters)]
        allDistances_df = DataFrameFactory.createDataFrame(allDistances, colNames)
        print("kmean centroids and all distances completed after: ", (datetime.now() - startTime))

        # merge dataframes together
        data_withTokens_df = DataFrameFactory.joinDataFrames(data_df, tokens_df)
        data_withTokens_andDistanceToCentroids = DataFrameFactory.joinDataFrames(data_withTokens_df, allDistances_df)
        data_withTokens_andDistanceToCentroids_list = DataFrameFactory.convertDataFrameToList(data_withTokens_andDistanceToCentroids)
        print("merging dataframes completed after: ", (datetime.now() - startTime))

        # insert in Db
        if(updateDb):
            self.tastingNotesRepo.deleteAll()
            self.tastingNotesRepo.insertMany(data_withTokens_andDistanceToCentroids_list, insertManyInChunksOf)
            print("insert tasting notes in db completed after: ", (datetime.now() - startTime))
            self.clustersRepo.deleteAll()
            self.clustersRepo.insertMany(cluster_list, insertManyInChunksOf)
            print("insert clusters in db completed after: ", (datetime.now() - startTime))
