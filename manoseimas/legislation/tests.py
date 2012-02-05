# coding: utf-8

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
