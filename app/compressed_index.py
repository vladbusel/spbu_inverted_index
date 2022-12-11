from functools import reduce
import pickle
import os
from preprocessing import tokenize
from encoder import *

class CompressedIndex:
    def __init__(self, compression_type='delta'):
        self.compressed_index = {}
        self.compression_type = compression_type
        self.set_methods(compression_type)

    def size(self):
        return f"{np.sum(np.array([len(x) for x in list(self.compressed_index.values())]))/(2**20)} Mb"

    def compress(self, inverted_index):
        self.compressed_index = {}
        for token, ids in inverted_index.items():
            self.compressed_index[token] = list_compression(ids, self.compression_algorithm)

    def load_or_create(self, inverted_index):
        if not os.path.exists(f'./data/compressed_index_{self.compression_type}.pickle'):
            self.load()
        else:
            self.create(inverted_index)

    def create(self, inverted_index):
        self.compress(inverted_index)
        with open(f'data/compressed_index_{self.compression_type}.pickle', 'wb') as f:
            pickle.dump(self.compressed_index, f)

    def load(self):
        with open(f'data/compressed_index_{self.compression_type}.pickle', 'rb') as f:
            self.compressed_index = pickle.load(f)

    def set_methods(self, compression_type):
        if compression_type == 'delta':
            self.compression_algorithm = elias_delta
            self.decoding_method = decoding_delta_bytes
        elif compression_type == 'gamma':
            self.compression_algorithm = elias_gamma
            self.decoding_method = decoding_gamma_bytes
        else:
            raise Exception('Choose correct compression_type (delta, gamma)')  

    def search(self, query, search_type=None):
        tokens = tokenize(query)
        query_hash = { term: self.decoding_method(self.compressed_index[term]) for term in tokens if term in self.compressed_index }
        if search_type == 'AND':
            return reduce(lambda a, b: list(set(a) & set(b)), query_hash.values())
        if search_type == 'OR':
            return reduce(lambda a, b: list(set(a) | set(b)), query_hash.values())
        if search_type not in ('AND', 'OR'):
            return query_hash
