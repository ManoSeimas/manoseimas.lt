# -*- coding: utf-8 -*-
import re

date_re = re.compile(r'(\d{4})\s*m\.\s+(\w+)\s+(\d{1,2})\s+d\.', re.UNICODE)
month_names_map = {
    u'sausio':     1,
    u'vasario':    2,
    u'kovo':       3,
    u'balandžio':  4,
    u'gegužės':    5,
    u'birželio':   6,
    u'liepos':     7,
    u'rugpjūčio':  8,
    u'rugsėjo':    9,
    u'spalio':    10,
    u'lapkričio': 11,
    u'gruodžio':  12,
}
