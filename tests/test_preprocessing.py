import unittest
from app.preprocessing import *

class PreprocessingTests(unittest.TestCase):
    def test_tokenize_words(self):
        tokens = tokenize("""Example пример""")
        self.assertEqual(tokens, ['example', 'пример'])

    def test_tokenize_href(self):
        tokens = tokenize("""https://docs-python.ru""")
        self.assertEqual(tokens, ['httpsdocspythonru'])

    def test_tokenize_symbols_to_delete(self):
        tokens = tokenize("""!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»""")
        self.assertEqual(tokens, [])

    def test_tokenize_word_forms(self):
        tokens = tokenize("""Статья статьи статью статье статьей""")
        self.assertEqual(tokens, ['статья', 'статья', 'статья', 'статья', 'статья'])

    def test_tokenize_word_suffix(self):
        tokens = tokenize("""подготовленные""")
        self.assertEqual(tokens, ['подготовить', 'статья', 'статья', 'статья', 'статья'])
