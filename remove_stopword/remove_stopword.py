import sys
import re
import ast
from sklearn.feature_extraction.text import TfidfVectorizer

def load_grams(path):
        with open(path, encoding='utf8') as fr:
            words = fr.read()
        return words.splitlines()
class RemoveStopWord(object):
    def __init__(self, stopword_path='remove_stopword/Vietnamese_stopword.txt'):
        self.stopword = load_grams(stopword_path)
        #print(self.stopword)
    def remove_stopword_bydict(self, document):
        words = []
        for word in document:
            if word.lower().replace('_',' ') not in self.stopword:
                words.append(word.lower())
        return words
    def remove_stopword_byTFIDF(self, documents, threshold = 3):
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(documents)
        features = tfidf.get_feature_names()
        stopwords = []
        print(min(tfidf.idf_), max(tfidf.idf_), len(features))
        for index, feature in enumerate(features):
            if tfidf.idf_[index] <= threshold:
                stopwords.append(feature)
        return stopwords