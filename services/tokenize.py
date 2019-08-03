import nltk
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class TokenizeService:

    # returns a new DataFrame where every row is the TF-IDF tokenization of the collection passed in, with stopwords
    # consider Stemming: reducing similar words to a base stem) and
    # consiedr Word Categorizing: analyze sentences to categorize words like adjectives, nouns, ...
    @staticmethod   
    def tokenize(coll:any, stopWords: any = None, vocabulary: any = None):
        if(stopWords):
            vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words=stopWords)
        else:
            vectorizer = TfidfVectorizer(ngram_range=(1,1), vocabulary=vocabulary)
        tokens = vectorizer.fit_transform(coll).toarray()
        names = vectorizer.get_feature_names()
        print('{0} names found during tokenization'.format(names.__len__()))
        return tokens, names

    @staticmethod   
    def getTopTokenNames(tokens, names, limit):
        array = np.array(names)
        sorting = np.argsort(tokens).flatten()[::-1]
        return array[sorting][:limit]

    @staticmethod   
    def getKMean(dataFrame, numberOfClusters):
        kmeans = KMeans(n_clusters=numberOfClusters)
        alldistances = kmeans.fit_transform(dataFrame)
        np.round_(alldistances,3,alldistances)
        centroids = kmeans.cluster_centers_
        return centroids, alldistances