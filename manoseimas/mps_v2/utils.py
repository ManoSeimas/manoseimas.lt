# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 TILS <info@transparency.lt>
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

from __future__ import unicode_literals

import re


abbreviations = {
    'IVPK': 'Informacinės Visuomenės Plėtros Komitetas',
    'TM': 'Teisingumo Ministerija',
    'TD': 'Teisės Departamentas',
    'ETD': 'Europos Teisės Departamentas',
    'LR': 'Lietuvos Respublika',
    'LRS': 'Lietuvos Respublikos Seimas',
    'LRV': 'Lietuvos Respublikos Vyriausybė',
    'FM': 'Finansų Ministerija',
    'STT': 'Specialiųjų Tyrimų Tarnyba',
    'TTK': 'Teisės ir Teisėtvarkos Komitetas',
    'BFK': 'Biudžeto ir Finansų Komitetas',
}


def is_state_actor(actor):
    """Try to guess if this is a state actor.

        >>> is_state_actor('Vardenis Pavardenis')
        False

        >>> is_state_actor(u'UAB „Bendrovė“')
        False

        >>> is_state_actor(u'Seimo narys V. Pavardenis')
        True

        >>> is_state_actor(u'Lietuvos Respublikos Vyriausybė')
        True

        >>> is_state_actor(u'Europos Teisės departamentas prie Lietuvos Respublikos Teisingumo ministerijos')
        True

    """
    actor = actor.replace('- ', '')
    actor = re.sub(r'[-()]', '', actor)
    actor = ' '.join(abbreviations.get(word.upper(), word) for word in actor.split())
    actor = actor.lower()
    actor = actor.replace('s eimo', 'seimo')
    if actor.startswith('teikia:'):
        actor = actor[len('teikia:'):].lstrip()
    if 'olimpinis' in actor:
        return False
    if actor.endswith(('sąjunga', 'biuras', 'rūmai')):
        return False
    if actor.startswith('všį'):
        return False
    if 'ministerij' in actor or 'departament' in actor:
        return True
    if 'komitet' in actor:
        return True
    if actor.startswith((
            'lietuvos respublik',
            'respublikos prezident',
            'prezident',
            'seimo',
            'specialiųjų tyrimų tarnyb',
            'specialiųjų tyrimo tarnyb', # typo, I assume
            'viešųjų',
            'valstyb',
            'vyriausyb',
    )):
        return True
    if actor.endswith('komitetas'):
        return True
    return False
