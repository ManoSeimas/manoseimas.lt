# coding: utf-8

from __future__ import unicode_literals

import re

a_word_re = re.compile(r'\w+', re.UNICODE)


def get_words(text):
    return a_word_re.findall(text)


def get_word_count(text):
    return len(get_words(text))
