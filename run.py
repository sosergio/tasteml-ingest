import nltk
import json
import repositories.tastingNotes as TastingNotesRepo
import numpy as np
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer

def readJsonFile(path):
    # this would read the entire file and generate dataframe
    # data_df = pd.read_json("resources/winemag-data-130k-v2.json")
    with open(path) as json_file:  
        return json.load(json_file)

# returns a new list of wines that have more points than the one specified
def filterWithQuality(points:int, data:any):
    return list(filter(lambda x: int(x["points"]) > points, data))

# returns the first 'limit' items from the 'data'
def take(limit:int, data:any):
    return data[:limit]

# taekes away punctuation, capitalization, and generic stopwords
def getStopWords():
    domainStopWords = ["tannins","flavor","flavour","wine","hints","notes","aromas","character","bit","palate","flavors","drink","finish","fruit","offers","style","hint","drinkable","imported"]
    return text.ENGLISH_STOP_WORDS.union(["book"]).union(domainStopWords)

# returns a Pandas DataFrame from the list
def generateDataFrame(data:any):
    return pd.DataFrame(data)

# returns a new DataFrame where every row is the TF-IDF tokenization of the collection passed in, using the stopwords
def tokenize(coll:any, stopWords:any):
    vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=stopWords)
    tokens = vectorizer.fit_transform(coll).toarray()
    names = vectorizer.get_feature_names()
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
    return df.reset_index().to_dict(orient='records')

data = readJsonFile('resources/winemag-data-130k-v2.json')
data_topQuality = filterWithQuality(80, data)
data_limit10 = take(30, data_topQuality)
data_df = generateDataFrame(data_limit10)

# first pass tokenize
sw = getStopWords()
firstPass_tokens,firstPass_names = tokenize(data_df["description"], sw)

# second pass tokenize
firstPass_topNames = getTopTokenNames(firstPass_tokens, firstPass_names, 10)
sw = sw.union(firstPass_topNames)
secondPass_tokens, secondPass_names = tokenize(data_df["description"], sw)

tokens_df = createDataFrame(secondPass_tokens, secondPass_names)
data_withTokens_df = joinDataFrames(data_df, tokens_df)
data_withTokens_list = convertDataFrameToList(data_withTokens_df)

TastingNotesRepo.deleteAll()
TastingNotesRepo.insertMany(data_withTokens_list)