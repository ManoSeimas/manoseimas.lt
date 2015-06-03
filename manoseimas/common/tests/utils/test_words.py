# coding: utf-8

from __future__ import unicode_literals

import unittest

from manoseimas.scrapy import textutils


class WordCountTest(unittest.TestCase):
    def test_get_word_count(self):
        word_count = textutils.get_word_count('Žodžiai, lietuviškai.')
        self.assertEqual(word_count, 2)

    def test_get_words(self):
        words = textutils.get_words('Žodžiai, lietuviškai.')
        self.assertEqual(words, ['Žodžiai', 'lietuviškai'])
