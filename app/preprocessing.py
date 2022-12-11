from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def tokenize(text):
    res = []
    text = text.translate(str.maketrans(' ', ' ', punctuation()))
    tokens = word_tokenize(text, language="russian")
    for token in tokens:
        if token not in stopwords.words("russian"):
            token = morph.parse(token)[0].normal_form
            if len(token) > 0:
                res.append(token)
    return res
            

def punctuation():
    return r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»'
