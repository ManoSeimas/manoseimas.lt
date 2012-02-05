# coding: utf-8

import re

RE_SPLIT_LAW_NAME = re.compile(ur'(įstatymo|statuto|konstitucijos|kodekso)')


def normalize(name):
    return name.strip().lower()


def split_law_name(name):
    """Splits law name into chunks, that should match original law name."""
    name = normalize(name)
    position = 0
    split = []
    markersmap = {
        u'įstatymo': u'įstatymas',
        u'statuto': u'statutas',
        u'konstitucijos': u'konstitucija',
        u'kodekso': u'kodeksas',
    }
    for match in RE_SPLIT_LAW_NAME.finditer(name):
        marker = match.group()
        replacement = markersmap[marker]
        chunk = name[position:match.start()].strip() + u' ' + replacement
        split.append(chunk)
    return split
