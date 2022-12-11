from collections import defaultdict
from functools import reduce
from preprocessing import tokenize
from document import Document
import os
import pickle
import numpy as np


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)

    def __repr__(self):
        return str(self.index)

    def size(self):
        return f"{np.sum(np.array([32*len(x) for x in list(self.index.values())]))/(2**20)} Mb"

    def index_documents(self, limit=None):
        for _, document in Document.all(limit).iterrows():
            self.index_document(document)
        with open('data/index.pickle', 'wb') as f:
            pickle.dump(self.index, f)
    
    def index_document(self, document):
        for token in tokenize(document.content):
            if document.id not in self.index[token]:
                self.index[token].append(document.id)

    def search(self, query, search_type=None):
        tokens = tokenize(query)
        query_hash = { term: self.index[term] for term in tokens if term in self.index }
        if search_type == 'AND':
            return reduce(lambda a, b: list(set(a) & set(b)), query_hash.values())
        if search_type == 'OR':
            return reduce(lambda a, b: list(set(a) | set(b)), query_hash.values())
        if search_type not in ('AND', 'OR'):
            return query_hash

    def load_data(self):
        if os.path.exists('./data/index.pickle'):
            with open('data/index.pickle', 'rb') as f:
                self.index = pickle.load(f)
