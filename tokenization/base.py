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
        sign = [r"==>", r"->", r"\.\.\.", r">>"]
        digits = r"\d+([\.,_]\d+)+"
        #email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        #web = r"^(http[s]?:\/\/)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
        email = r"\S+@\S+"
        web = r'((www\.[^\s]+)|(https?://[^\s]+))'
        datetime = [
            r"\d{1,2}\/\d{1,2}(\/\d+)?",
            r"\d{1,2}-\d{1,2}(-\d+)?",
        ]
        word = r"\w+"
        #non_word = r"[^\w\s]"
        abbreviations = [
            r"[A-ZĐ]+\.",
            r"Tp\.",
            r"Mr\.", r"Mrs\.", r"Ms\.",
            r"Dr\.", r"ThS\."
        ]
        patterns = []
        patterns.extend(abbreviations)
        patterns.extend(sign)
        patterns.extend([web, email])
        patterns.extend(datetime)
        patterns.extend([digits, word])
        patterns = "(" + "|".join(patterns) + ")"
        if sys.version_info < (3, 0):
            patterns = patterns.decode('utf-8')
        tokens = re.findall(patterns, text, re.UNICODE)
        return [token[0] for token in tokens]
