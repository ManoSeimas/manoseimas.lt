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
