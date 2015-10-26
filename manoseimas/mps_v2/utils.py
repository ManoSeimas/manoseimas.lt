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

known_state_actors = [
    'A. Jusevičienė',   # dirba VRM
    'A. Norkūnas',      # teisėjas
    'A. Vaičiulis',     # buvęs policijos viršininkas?
    'D. Komparskienė',  # Teisės ir teisėtvarkos komiteto biuro vedėja
    'I. Bazylevas',     # dirba VRM VSD
    'J. Sykas',         # prokuroras
    'K. Daukšys',       # seimo narys
    'M. Bastys',        # seimo narys
    'M. Zasčiurinskas', # seimo narys
    'V. Stundys',       # seimo narys
    'Vida Jakiūnaitė',  # politikė?
    '„LATGA“',          # uhh
]


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
    actor = actor.lower()
    if 'olimpinis' in actor:
        return False
    if actor.endswith(('sąjunga', 'biuras', 'rūmai')):
        if actor.startswith('jungtinių tautų'):
            return True
        if 'policijos biuras' in actor:
            return True
        if actor.startswith('nacionalinis'):
            return True
        return False
    if actor.startswith(('všį', 'valstybės įmonė')):
        if 'klinik' in actor:
            return True
        if 'kraujo centr' in actor:
            return True
        if 'patologijos centr' in actor:
            return True
        return False
    if ' neetatin' in actor:
        return False
    if 'darbdavių konfederac' in actor:
        return False
    if 'ministerij' in actor or 'departament' in actor:
        return True
    if 'komitet' in actor:
        return True
    if 'savivaldyb' in actor:
        if 'asociac' in actor:
            return False
        return True
    if 'plėtros taryb' in actor:
        return True
    if 'regioninio parko direkcij' in actor:
        return True
    if 'kultūros globos taryb' in actor:
        return True
    if 'konkurencijos taryb' in actor:
        return True
    if 'policijos tarnyb' in actor:
        return True
    if 'kriminalinė tarnyb' in actor:
        return True
    if 'gyventojų registro tarnyb' in actor:
        return True
    if 'lygių galimybių kontrolieriaus tarnyb' in actor:
        return True
    if actor.endswith('teismas'):
        return True
    if actor.endswith('komisija'):
        if actor == 'lietuvos radijo ir televizijos komisija':
            return False
        if actor.startswith('pasipriešinimo'):
            return False
        return True
    if actor.endswith(' meras'):
        return True
    if 'prokuratūr' in actor:
        return True
    if actor.startswith('teikia '):
        actor = actor[len('teikia '):]
    if actor.endswith('asociacija'):
        if actor == 'lietuvos respublikos teisėjų asociacija':
            return True
        return False
    if 'gretutinių teisių asociacija „agata“' in actor:
        return True
    if actor.endswith('mokyklos'):
        return True
    if actor.startswith('nacional'):
        if actor.endswith(('susivienijimas', 'asociacija', 'koalicija',
                           'laureatai', 'platforma')):
            return False
        return True
    if actor.startswith((
            'lietuvos respublik',
            'respublikos prezident',
            'prezident',
            'seimo',
            'specialiųjų tyrimų tarnyb',
            'viešųjų',
            'valstyb',
            'vyriausyb',
            'darbo grup',
            'lietuvos bank',
            'europos centrinis bank',
            'europos sisteminės rizikos valdyba',
            'teisėj',
            'spaudos, radijo ir televizijos rėmimo fondas',
            'užkrečiamųjų ligų ir aids centras',
            'žemės ūkio rūmų taryba',
    )):
        return True
    for known in known_state_actors:
        if actor.startswith(known.lower()):
            return True
    return False
