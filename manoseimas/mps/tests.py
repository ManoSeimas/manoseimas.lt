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

from django.test import TestCase

from mock import Mock

from sboard.models import couch
from sboard.tests import NodesTestsMixin

from .management.commands.syncmps import SyncProcessor


class TestSync(NodesTestsMixin, TestCase):
    def test_sync(self):
        jursenas = {
            u'id': u'110p',
            u'key': u'110p',
            u'value': {u'rev': u'1-62c1a003a5a377cdf154f200cf25c27b'},
            u'doc': {
                u'_id': u'110p',
                u'_rev': u'1-62c1a003a5a377cdf154f200cf25c27b',
                u'candidate_page': (u'http://www.vrk.lt/rinkimai/400_lt/'
                                    u'Kandidatai/Kandidatas22411/'
                                    u'Kandidato22411Anketa.html'),
                u'constituency': u'pagal sąrašą',
                u'dob': u'1938-05-18',
                u'doc_type': u'person',
                u'email': [u'Ceslovas.Jursenas@lrs.lt', u'cejurs@lrs.lt'],
                u'first_name': u'Česlovas',
                u'last_name': u'Juršėnas',
                u'home_page': (u'http://www3.lrs.lt/pls/inter/w5_show?'
                               u'p_r=4487&p_k=1'),

                u'groups': [
                    {
                        u'membership': [u'2008-11-17', None],
                        u'name': u'2008-2012',
                        u'position': u'seimo narys',
                        u'type': u'parliament',
                    },
                    {
                        u'name': u'Lietuvos socialdemokrat\u0173 partija',
                        u'type': u'party',
                    },
                    {
                        u'membership': [u'2008-11-18', None],
                        u'name': u'Žmogaus teisių komitetas',
                        u'position': u'Komiteto narys',
                        u'source': (u'http://www3.lrs.lt/pls/inter/w5_show?'
                                    u'p_r=6113&p_k=1&p_a=6&p_pad_id=48&'
                                    u'p_kade_id=6'),
                        u'type': u'committee',
                    },
                    {
                        u'membership': [u'2008-12-04', None],
                        u'name': (u'Seimo delegacija Lietuvos Respublikos '
                                  u'Seimo ir Lenkijos Respublikos Seimo ir '
                                  u'Senato narių asamblėjoje'),
                        u'position': u'narys',
                        u'source': (u'http://www3.lrs.lt/pls/inter/w5_show?'
                                    u'p_r=6113&p_k=1&p_a=7&p_seim_n_gr_id=15'),
                        u'type': u'group',
                    },
                ],
                u'parliament': [u'2008-2012', u'2004-2008', u'2000-2004',
                                u'1996-2000', u'1992-1996', u'1990-1992'],
                u'phone': [u'2396025', u'2396626'],
                u'photo': (u'http://www3.lrs.lt/home/seimo_nariu_nuotraukos/'
                           u'2008/ceslovas_jursenas.jpg'),
                u'raised_by': u'Lietuvos socialdemokratų partija',
                u'source': {
                    u'id': u'110',
                    u'name': u'lrslt',
                    u'url': (u'http://www3.lrs.lt/pls/inter/w5_show?'
                             u'p_a=5&p_asm_id=110&p_k=1&p_kade_id=6&p_r=6113'),
                },
                u'updated': u'2012-04-20T23:25:34.432432',
            },
        }

        db = Mock()
        db.view.return_value = [jursenas]
        db.save_doc.return_value = True

        processor = SyncProcessor(db, verbosity=0)
        processor.sync()

        node = couch.by_slug(key='ceslovas-jursenas').one()
        self.assertEqual(node.first_name, u'Česlovas')
        self.assertEqual(node.last_name, u'Juršėnas')
        self.assertEqual(node.keywords, ['ceslovas', 'jursenas'])
