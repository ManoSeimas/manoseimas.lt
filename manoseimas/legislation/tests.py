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

import StringIO
import unittest

from mock import patch

from django.test import TestCase

from sboard.models import get_new_id
from sboard.tests import NodesTestsMixin

from manoseimas.legislation.management.commands.syncsittings import RawVoting
from manoseimas.mps.models import MPProfile
from manoseimas.scrapy.tests.mps import parse_mp
from manoseimas.scrapy.tests.pipeline import FakePipeline
from manoseimas.scrapy.tests.sittings import parse_question
from manoseimas.scrapy.tests.sittings import parse_voting

import manoseimas.legislation.management.commands.syncsittings as syncsittings
import manoseimas.mps.management.commands.syncmps as syncmps

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


class FakeSyncProcessor(syncsittings.SyncProcessor):
    def __init__(self, *args, **kwargs):
        super(FakeSyncProcessor, self).__init__(*args, **kwargs)
        self._fraction_ids = {}
        self._nodes = []

    def _get_or_add(self, ids, key):
        if key not in ids:
            ids[key] = get_new_id()
        return ids[key]

    def get_profile_id(self, profile_source_id):
        return self._get_or_add(self._profile_ids, profile_source_id)

    def get_fraction_id(self, fraction_abbreviation):
        return self._get_or_add(self._fraction_ids, fraction_abbreviation)

    def save_node(self, node):
        self._nodes.append(node)


class TestSyncSittings(NodesTestsMixin, TestCase):
    def test_sync(self):
        pipeline = FakePipeline()

        items = parse_question()
        # question
        pipeline.process_item(items[0], None)
        # voting details from question agenda
        pipeline.process_item(items[1], None)

        items = parse_voting()
        # list of votings
        voting = pipeline.process_item(items[0], None)

        voting = RawVoting(dict(voting))

        processor = FakeSyncProcessor()
        processor.sync([voting])

        node = processor._nodes[0]
        profile_id = processor.get_profile_id('47852')
        self.assertEqual(node.votes['aye'][0][0], profile_id)

    @patch.object(syncmps.SyncProcessor, 'fetch_photo')
    def test_get_profile_by_source_id(self, fetch_photo):
        fetch_photo.return_value = StringIO.StringIO('content')

        pipeline = FakePipeline()
        pipeline.process_item(parse_mp(), None)
        doc = pipeline._stored_items['53911p']

        db = MPProfile.get_db()
        processor = syncmps.SyncProcessor(db, verbosity=0)
        processor.process(doc)

        processor = syncsittings.SyncProcessor()
        node_id = processor.get_profile_id('53911')

        self.assertEqual(node_id, '000005')
