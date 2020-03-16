import re
import sys
import ast
import unicodedata as ud

def load_grams(path):
    with open(path, encoding='utf8') as fr:
        words = fr.read()
        words = ast.literal_eval(words)
    return words

def syllablize(text):
        """
        tách thành các âm
        """
        text = ud.normalize('NFC', text)
        digits = r"\d+([\.,_]\d+)+"
        email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        #email = r"\S+@\S+"
        web = r'((www\.[^\s]+)|(https?://[^\s]+))'
        datetime = [
            r"\d{1,2}\/\d{1,2}(\/\d+)?",
            r"\d{1,2}-\d{1,2}(-\d+)?",
        ]
        word = r"\w+"
        abbreviations = [
            r"[A-ZĐ]+\.",
            r"Tp\.",
            r"Mr\.", r"Mrs\.", r"Ms\.",
            r"Dr\.", r"ThS\."
        ]
        patterns = []
        patterns.extend(abbreviations)
        patterns.extend([web, email])
        patterns.extend(datetime)
        patterns.extend([digits, word])
        patterns = "(" + "|".join(patterns) + ")"
        if sys.version_info < (3, 0):
            patterns = patterns.decode('utf-8')
        tokens = re.findall(patterns, text, re.UNICODE)
        return [token[0] for token in tokens]
