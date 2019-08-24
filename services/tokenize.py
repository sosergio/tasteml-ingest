import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
import string
from nltk.stem.porter import PorterStemmer

class TokenizeService:

    def __init__(self, printDebug: bool):
        self.printDebug = printDebug
        self.stemmer = PorterStemmer()

    def stemListOfTokens(self, list):
        words = []
        for token in list:
            if token in string.punctuation:
                continue
            if token.endswith('y'):
                token = token[:-1]
            words.append(self.stemmer.stem(token))
        if(self.printDebug):
            print(words)
        return words

    def stemAndTokenizeText(self, text):
        text = text.lower()
        return self.stemListOfTokens(nltk.word_tokenize(text))

    # returns a new DataFrame where every row is the TF-IDF tokenization of the collection passed in, with stopwords
    # consider Stemming: reducing similar words to a base stem
    # consider Word Categorizing: analyze sentences to categorize words like adjectives, nouns, ...
    def tfidfTokenize(self, coll: any, stopWords: any = None, vocabulary: any = None, tokenizer: any = None):
        if(stopWords):
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1), stop_words=stopWords, tokenizer=tokenizer)
        else:
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1), vocabulary=vocabulary, tokenizer=tokenizer)
        tokens = vectorizer.fit_transform(coll).toarray()
        names = vectorizer.get_feature_names()
        return tokens, names

    def getTopTokenNames(self, tokens, names, limit):
        array = np.array(names)
        sorting = np.argsort(tokens).flatten()[::-1]
        return array[sorting][:limit]

    def kmeanCluster(sefl, dataFrame, numberOfClusters):
        kmeans = KMeans(n_clusters=numberOfClusters)
        alldistances = kmeans.fit_transform(dataFrame)
        np.round_(alldistances, 3, alldistances)
        centroids = kmeans.cluster_centers_
        return centroids, alldistances
