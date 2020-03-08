import os, sys
sys.path.append('./tokenization')
sys.path.append('./remove_stopword')
from LongMatching import PhraseTokenization
from remove_stopword import RemoveStopWord
from nltk.tokenize import sent_tokenize
import numpy as np

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
    sent2vec = np.zeros(len(text_dict))
    for phrase in phrases:
        sent2vec[text_dict.index(phrase)]+=1
    return sent2vec

def get_vec_from_doc(text):
    '''
    Lấy vecto đặc trưng của tất cả câu
    '''
    sents = sent_tokenize(text)
    text_dict = create_dict_from_Doc(text)
    sent2vec = []
    for sent in sents:
        sent2vec.append(convert_sent_to_vec(sent, text_dict))
    return sent2vec