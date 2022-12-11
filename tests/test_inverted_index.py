import unittest
from app.encoder import *
from app.inverted_index import InvertedIndex
from collections import defaultdict

import pandas as pd


class InvertedIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inverted_index = InvertedIndex()

    def test_index_document(self):
        doc = pd.DataFrame({"id": [1], "content": ["lalala"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.assertEqual(self.inverted_index, defaultdict(list, {'lalala': [1]}))

    def test_index_duplicated_document(self):
        doc = pd.DataFrame({"id": [1], "content": ["lalala"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.inverted_index.index_document(doc)
        self.assertEqual(self.inverted_index, defaultdict(list, {'lalala': [1]}))

    def test_search_same_text(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.assertEqual(self.inverted_index.search('some_text'), {'some_test': [1]})

    def test_search_other_text(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.assertEqual(self.inverted_index.search('other_text'), {})

    def test_search_with_AND(self):
        docs = pd.DataFrame({"id": [1,2], "content": ["some test", "other test"]})
        self.inverted_index.index_document(docs.iloc[0])
        self.inverted_index.index_document(docs.iloc[1])
        self.assertEqual(self.inverted_index.search('some test', search_type="AND"), [1])

    def test_search_with_OR(self):
        docs = pd.DataFrame({"id": [1,2], "content": ["some test", "other test"]})
        self.inverted_index.index_document(docs.iloc[0])
        self.inverted_index.index_document(docs.iloc[1])
        self.assertEqual(self.inverted_index.search('some test', search_type="OR"), [1,2])

    def test_size(self):
        doc = pd.DataFrame({"id": [1], "content": ["some_test"]}).iloc[0]
        self.inverted_index.index_document(doc)
        self.assertEqual(self.inverted_index.size, '3.0517578125e-05 Mb')
