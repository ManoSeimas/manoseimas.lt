# coding: utf-8

# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.


import re

RE_CLEAN_NON_ALPHA = re.compile(r'\W+', re.UNICODE)

SKIP_WORDS = (u'ir', u'frakcija')

COMPOUND_WORDS = (u'social',)

FRACTION_ABBR_EXCEPTIONS = {
    u'mišri seimo narių grupė': u'MG',
    (u'jungtinė liberalų ir centro sąjungos ir tautos prisikėlimo partijos '
     u'frakcija'): u'JF',
    (u'tėvynės sąjungos frakcija'): u'TSLKDF',
    (u'Tėvynės sąjungos-Lietuvos krikščionių demokratų frakcija'): u'TSLKDF',
    (u'Lietuvos lenkų rinkimų akcijos-Krikščioniškų šeimų sąjungos frakcija'): u'LLRAKŠSF',
    (u'Lietuvos lenkų rinkimų akcijos frakcija'): u'LLRAKŠSF',
}


def clean_title(title):
    return RE_CLEAN_NON_ALPHA.sub(' ', title).lower()


def split_compound_word(word, compound_words=COMPOUND_WORDS):
    ret = []
    for compound in compound_words:
        if word.startswith(compound):
            ret.append(compound)
            ret.append(word[len(compound):])
    return ret


def split_words(title, compound_words=COMPOUND_WORDS):
    for word in title.split(' '):
        compound = split_compound_word(word, compound_words)
        if compound:
            for word in compound:
                yield word
        else:
            yield word


def get_fraction_abbr(title, skip=SKIP_WORDS, compound_words=COMPOUND_WORDS):
    letters = []
    title = clean_title(title)

    if title in FRACTION_ABBR_EXCEPTIONS:
        return FRACTION_ABBR_EXCEPTIONS[title]

    for word in split_words(title, compound_words):
        if word and word not in skip:
            letters.append(word[0].upper())

    letters.append(u'F')
    return u''.join(letters)
