import sys
import re
from base import load_grams, syllablize

class PhraseTokenization(object):
    def __init__(self, bi_grams_path = 'tokenization/bi_grams.txt', tri_grams_path = 'tokenization/tri_grams.txt'):
        self.bi_grams = load_grams(bi_grams_path)
        self.tri_grams = load_grams(tri_grams_path)
    def phrase_tokenize(self, text):
        '''
        Tách các từ tiếng Việt
        '''
        syllables = syllablize(text)
        syll_len = len(syllables)
        word_list = []
        cur_word_id = 0
        while cur_word_id < syll_len:
            cur_word = syllables[cur_word_id]
            if cur_word_id == (syll_len-1):
                word_list.append(cur_word)
                cur_word_id += 1
            elif cur_word_id == (syll_len - 2):
                next_word = syllables[cur_word_id + 1]
                if ' '.join([cur_word.lower(), next_word.lower()]) in self.bi_grams:
                    word_list.append(' '.join([cur_word, next_word]))
                else:
                    word_list.append(cur_word)
                    word_list.append(next_word)
                cur_word_id += 2
            else:
                next_word = syllables[cur_word_id + 1]
                third_word = syllables[cur_word_id + 2]
                if ' '.join([cur_word.lower(), next_word.lower(), third_word.lower()]) in self.tri_grams:
                    word_list.append(' '.join([cur_word, next_word, third_word]))
                    cur_word_id += 3
                elif ' '.join([cur_word.lower(), next_word.lower()]) in self.bi_grams:
                    word_list.append(' '.join([cur_word, next_word]))
                    cur_word_id += 2
                else:
                    word_list.append(cur_word)
                    cur_word_id += 1
        return word_list
