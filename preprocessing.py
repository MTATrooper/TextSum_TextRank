import os, sys
sys.path.append('./tokenization')
sys.path.append('./remove_stopword')
from LongMatching import PhraseTokenization
from remove_stopword import RemoveStopWord
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
import math
from gensim.models import KeyedVectors
from vncorenlp import VnCoreNLP

def computeVec(text):
    annotator = VnCoreNLP("../VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')
    w2v = KeyedVectors.load_word2vec_format("../Word2vec_Model/wiki.vi.model.bin", binary=True)
    vocab = w2v.vocab
    sentences = sent_tokenize(text)
    X = []
    for sentence in sentences:
        words = annotator.tokenize(sentence)
        #print(words)
        sentence_vec = np.zeros((400))
        count = 0
        for word in words[0]:
            if word.lower() in vocab:
                count += 1
                sentence_vec+=w2v[word.lower()]
        X.append(sentence_vec/count)
    return X

def create_dict_from_Doc(text):
    '''
    Tạo từ điển của văn bản
    '''
    sentenses = sent_tokenize(text)
    token = PhraseTokenization() 
    textClean = RemoveStopWord()
    text_dict = []
    for sentense in sentenses:
        phrases = token.phrase_tokenize(sentense)
        phrases = textClean.remove_stopword_bydict(phrases)
        for phrase in phrases:
            text_dict.append(phrase)
    text_dict = list(set(text_dict))
    text_dict.sort()
    return text_dict

def convert_sent_to_vec(sent, text_dict):
    '''
    tạo vecto đặc trưng của mỗi câu trong văn bản theo Bag of word
    '''
    token = PhraseTokenization() 
    textClean = RemoveStopWord()
    phrases = token.phrase_tokenize(sent)
    phrases = textClean.remove_stopword_bydict(phrases)
    sent2vec = np.zeros(len(text_dict), dtype=float)
    for phrase in phrases:
        sent2vec[text_dict.index(phrase)]+=1
    return sent2vec

def get_vec_from_doc(text):
    '''
    Lấy vecto BOW của tất cả câu
    '''
    sents = sent_tokenize(text)
    text_dict = create_dict_from_Doc(text)
    sent2vec = []
    for sent in sents:
        sent2vec.append(convert_sent_to_vec(sent, text_dict))
    return sent2vec

def computeTF(lstVec):
    lstResult = np.zeros((len(lstVec), len(lstVec[0])))
    for i in range(len(lstVec)):
        sent_length = 0
        for j in range(len(lstVec[i])):
            sent_length += lstVec[i][j]
        for j in range(len(lstVec[i])):
            lstResult[i][j] = lstVec[i][j]/sent_length
    return lstResult

def computeIDF(lstVec):
    N = len(lstVec)
    lstResult = np.zeros((len(lstVec), len(lstVec[0])))
    for i in range(len(lstVec)):
        for j in range(len(lstVec[i])):
            if lstVec[i][j] != 0:
                count = 0
                for vec in lstVec:
                    if vec[j] != 0: count += 1
                lstResult[i][j] = math.log10(N/count)
    return lstResult

def computeTFIDF(lstVec):
    lstVecTF = computeTF(lstVec)
    lstVecIDF = computeIDF(lstVec)
    for i in range(len(lstVec)):
        for j in range(len(lstVec[i])):
            lstVec[i][j] = lstVecTF[i][j] * lstVecIDF[i][j]
    return lstVec