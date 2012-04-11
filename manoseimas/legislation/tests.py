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

import unittest

from .management.commands.synclegalacts import Command
from .models import Law, LawChange, LawProject
from .utils import split_law_name


class SyncLegalActsTest(unittest.TestCase):
    def test_splitter(self):
        name = (u'Piliečių įstatymų leidybos iniciatyvos įstatymo 9 '
                u'straipsnio pakeitimo įstatymo projektas')
        self.assertEqual(split_law_name(name), [
            (u'piliečių įstatymų leidybos iniciatyvos įstatymas'),
            (u'piliečių įstatymų leidybos iniciatyvos įstatymo 9 straipsnio '
             u'pakeitimo įstatymas'),
        ])

        name = (u'Tarnybos Kalėjimų departamente prie Lietuvos Respublikos '
                u'teisingumo ministerijos statuto pakeitimo įstatymo 1 '
                u'straipsnio pakeitimo įstatymo 3 straipsnio pakeitimo '
                u'įstatymo projektas')
        self.assertEqual(split_law_name(name), [
            (u'tarnybos kalėjimų departamente prie lietuvos respublikos '
             u'teisingumo ministerijos statutas'),
            (u'tarnybos kalėjimų departamente prie lietuvos respublikos '
             u'teisingumo ministerijos statuto pakeitimo įstatymas'),
            (u'tarnybos kalėjimų departamente prie lietuvos respublikos '
             u'teisingumo ministerijos statuto pakeitimo įstatymo 1 '
             u'straipsnio pakeitimo įstatymas'),
            (u'tarnybos kalėjimų departamente prie lietuvos respublikos '
             u'teisingumo ministerijos statuto pakeitimo įstatymo 1 '
             u'straipsnio pakeitimo įstatymo 3 straipsnio pakeitimo '
             u'įstatymas')
        ])

        name = u'Žemės ūkio bendrovių įstatymas'
        self.assertEqual(split_law_name(name), [])

    def test_sync(self):
        cmd = Command()
