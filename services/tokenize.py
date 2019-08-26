import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import MWETokenizer


class TokenizeService:

    def __init__(self, printDebug: bool):
        self.printDebug = printDebug
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.mweTokenizer = MWETokenizer(separator=' ')
        self.tag_dict = {"J": wordnet.ADJ,
                         "N": wordnet.NOUN,
                         "V": wordnet.VERB,
                         "R": wordnet.ADV}

    def get_wordnet_pos(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        return self.tag_dict.get(tag, wordnet.NOUN)

    def lemmaTokenize(self, tokens):
        words = []
        for token in tokens:
            if token in string.punctuation:
                continue
            words.append(self.lemmatizer.lemmatize(
                token, self.get_wordnet_pos(token)))
        return words

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
        # generates mono-gram tokens
        monograms = nltk.word_tokenize(text)
        # stems the tokens
        # return self.stemListOfTokens(monograms)
        # lemmatization ot the tokens
        monograms = self.lemmaTokenize(monograms)
        # generates n-gram tokens
        tokens = self.mweTokenizer.tokenize(monograms)
        if(self.printDebug):
            print(tokens)
        return tokens

    def addMweFromVocabulary(self, vocabulary):
        [self.mweTokenizer.add_mwe(t.split(' '))
            for t in vocabulary
            if ' ' in t]

    # returns a new DataFrame where every row is the TF-IDF tokenization of the collection passed in, with stopwords
    # consider Stemming: reducing similar words to a base stem
    # consider Word Categorizing: analyze sentences to categorize words like adjectives, nouns, ...
    def tfidfTokenize(self, coll: any, stopWords: any = None, vocabulary: any = None, tokenizer: any = None):
        if(stopWords):
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1), stop_words=stopWords, tokenizer=tokenizer)
        else:
            self.addMweFromVocabulary(vocabulary)
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1), vocabulary=vocabulary, tokenizer=tokenizer)
        tokens = vectorizer.fit_transform(coll).toarray()
        names = vectorizer.get_feature_names()
        return tokens, names

    def getTopTokenNames(self, tokens, names, limit):
        array = np.array(names)
        sorting = np.argsort(tokens).flatten()[::-1]
        return array[sorting][:limit]

    def kmeanCluster(self, dataFrame, numberOfClusters):
        kmeans = KMeans(n_clusters=numberOfClusters)
        alldistances = kmeans.fit_transform(dataFrame)
        np.round_(alldistances, 3, alldistances)
        centroids = kmeans.cluster_centers_
        np.round_(centroids, 3, centroids)
        return centroids, alldistances

    def gaussianCluster(self, dataFrame, numberOfClusters):
        gmm = GaussianMixture(n_components=numberOfClusters,
                              covariance_type='full').fit(dataFrame)
        alldistances = gmm.predict_proba(dataFrame)
        np.round_(alldistances, 3, alldistances)
        centroids = gmm.means_
        np.round_(centroids, 3, centroids)
        return centroids, alldistances
