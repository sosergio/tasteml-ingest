import nltk
import json
import repositories.tastingNotes as TastingNotesRepo
import repositories.tags as TagsRepo
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

def readJsonFile(path):
    # this would read the entire file and generate dataframe
    # data_df = pd.read_json("resources/winemag-data-130k-v2.json")
    with open(path) as json_file:  
        return json.load(json_file)

# returns a new list of wines that have more points than the one specified
def filterWithQuality(points:int, data:any):
    return list(filter(lambda x: int(x["points"]) > points, data))

# returns the first "limit" items from the "data"
def take(limit:int, data:any):
    return data[:limit]

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

# returns a Pandas DataFrame from the list
def generateDataFrame(data:any):
    return pd.DataFrame(data)

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

def createDataFrame(values, cols):
    return pd.DataFrame(values, columns=cols)

# returns a new dataframe which is the concatenation of the ones passed
def joinDataFrames(df1, df2):
    return pd.concat([df1, df2], axis=1)

def convertDataFrameToList(df:any):
    return df.reset_index().to_dict(orient="records")

def getKMean(dataFrame, numberOfClusters):
    kmeans = KMeans(n_clusters=numberOfClusters)
    alldistances = kmeans.fit_transform(dataFrame)
    np.round_(alldistances,3,alldistances)
    centroids = kmeans.cluster_centers_
    return centroids, alldistances

startTime = datetime.now()

sampleCount = 50000
firstPassExcludeTopNamesCount = 0
numberOfClusters = 25
insertManyInChunksOf = 250
updateDb = True
runTwoPassOfTokenize = False

data = readJsonFile("resources/winemag-data-130k-v2.json")
flavours_dict = readJsonFile("resources/flavours.json")
data_topQuality = filterWithQuality(80, data)
print("items with top quality", data_topQuality.__len__())
data_sample = take(sampleCount, data_topQuality)
data_df = generateDataFrame(data_sample)
# remove rows wich have nulls
data_df.dropna()
# transform points column from string to numbers
data_df["points"] = data_df["points"].apply(pd.to_numeric)
# attach a column for quality/price ratio
data_df['ratio'] = data_df.apply(lambda row: row.points/row.price, axis=1)
print("load file completed after: ", (datetime.now() - startTime))

# first pass tokenize
stopWords = getStopWords()
tokens, names = tokenize(data_df["description"], None, flavours_dict)
print("first pass tokenize completed after: ", (datetime.now() - startTime))

# second pass tokenize
if(runTwoPassOfTokenize):
    firstPass_topNames = getTopTokenNames(tokens, names, firstPassExcludeTopNamesCount)
    print("firstPass_topNames: ", firstPass_topNames)
    stopWords = stopWords + list(firstPass_topNames[:50])
    tokens, names = tokenize(data_df["description"], stopWords, None)

tokens_df = createDataFrame(tokens, names)
print("second pass tokenize and dataframe completed after: ", (datetime.now() - startTime))

# calculate the kmean centroids and all distances (item to centroids)
centroids, allDistances = getKMean(tokens_df, numberOfClusters)
cluster_df = createDataFrame(centroids, names)
cluster_list = convertDataFrameToList(cluster_df)
colNames = ['to_{0}'.format(s) for s in range(numberOfClusters)]
allDistances_df = createDataFrame(allDistances, colNames)
print("kmean centroids and all distances completed after: ", (datetime.now() - startTime))

# merge dataframes together
data_withTokens_df = joinDataFrames(data_df, tokens_df)
data_withTokens_andDistanceToCentroids = joinDataFrames(data_withTokens_df, allDistances_df)
data_withTokens_andDistanceToCentroids_list = convertDataFrameToList(data_withTokens_andDistanceToCentroids)
print("merging dataframes completed after: ", (datetime.now() - startTime))

# insert in Db
if(updateDb):
    TastingNotesRepo.deleteAll()
    TastingNotesRepo.insertMany(data_withTokens_andDistanceToCentroids_list, insertManyInChunksOf)
    print("insert tasting notes in db completed after: ", (datetime.now() - startTime))
    TagsRepo.deleteAll()
    TagsRepo.add(names)
    print("insert tags in db completed after: ", (datetime.now() - startTime))
    ClustersRepo.deleteAll()
    ClustersRepo.insertMany(cluster_list, insertManyInChunksOf)
    print("insert clusters in db completed after: ", (datetime.now() - startTime))
