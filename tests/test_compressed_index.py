import unittest
from app.encoder import *
from app.inverted_index import InvertedIndex
from app.compressed_index import CompressedIndex
from collections import defaultdict

import pandas as pd


class CompressedIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gamma_compressed_index = CompressedIndex('gamma')
        self.delta_compressed_index = CompressedIndex('delta')
        self.inverted_index = InvertedIndex()

    def test_index_document_gamma(self):
        doc = pd.DataFrame({"id": [1], "content": ["lalala"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.gamma_compressed_index.compress(self.inverted_index)
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.compressed_index, {'lalala': b'010'})

    def test_index_document_delta(self):
        doc = pd.DataFrame({"id": [1], "content": ["lalala"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.gamma_compressed_index.compress(self.inverted_index)
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.delta_compressed_index.compressed_index, {'lalala': b'0100'})

    def test_search_same_text_gamma(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.gamma_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.search('some_text'), {'some_test': [1]})

    def test_search_same_text_delta(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.delta_compressed_index.search('some_text'), {'some_test': [1]})

    def test_search_other_text_gamma(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.gamma_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.search('other_text'), {})

    def test_search_other_text_delta(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.search('other_text'), {})

    def test_search_with_AND_gamma(self):
        docs = pd.DataFrame({"id": [1,2], "content": ["some test", "other test"]})
        self.inverted_index.index_document(docs.iloc[0])
        self.inverted_index.index_document(docs.iloc[1])
        self.gamma_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.search('some test', search_type="AND"), [1])

    def test_search_with_AND_delta(self):
        docs = pd.DataFrame({"id": [1,2], "content": ["some test", "other test"]})
        self.inverted_index.index_document(docs.iloc[0])
        self.inverted_index.index_document(docs.iloc[1])
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.delta_compressed_index.search('some test', search_type="AND"), [1])
    
    def test_search_with_OR_gamma(self):
        docs = pd.DataFrame({"id": [1,2], "content": ["some test", "other test"]})
        self.inverted_index.index_document(docs.iloc[0])
        self.inverted_index.index_document(docs.iloc[1])
        self.gamma_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.search('some test', search_type="OR"), [1,2])

    def test_search_with_OR_delta(self):
        docs = pd.DataFrame({"id": [1,2], "content": ["some test", "other test"]})
        self.inverted_index.index_document(docs.iloc[0])
        self.inverted_index.index_document(docs.iloc[1])
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.delta_compressed_index.search('some test', search_type="OR"), [1,2])

    def test_size_gamma(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.gamma_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.gamma_compressed_index.size, '2.86102294921875e-06 Mb')

    def test_size_delta(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.delta_compressed_index.compress(self.inverted_index)
        self.assertEqual(self.delta_compressed_index.size, '3.814697265625e-06 Mb')
