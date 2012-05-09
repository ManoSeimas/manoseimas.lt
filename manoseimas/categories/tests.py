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

import os
from unittest import TestCase

from couchdbkit import Server, push

from django.template.loader import render_to_string

from manoseimas.categories.models import iterate_tree


class TestTree(TestCase):

    def setUp(self):
        self.server = Server()
        self.dbname = 'unittests_tree'
        self.db = db = self.server.create_db(self.dbname)

        db['a'] = {'name': 'a'}
        db['b'] = {'name': 'b', 'parents': ['a']}
        db['c'] = {'name': 'c', 'parents': ['a', 'b']}
        db['d'] = {'name': 'd'}
        db['e'] = {'name': 'e', 'parents': ['d']}

        docid = "_design/tests"
        app_path = os.path.dirname(__file__)
        push(os.path.join(app_path, "_design"), db, force=True, docid=docid)

    def tearDown(self):
        self.server.delete_db(self.dbname)

    def test_iterate_tree(self):
        view = self.db.view('tests/tree', include_docs=True)
        string = render_to_string('manoseimas/categories/tree.html', {
                'tree': iterate_tree(view),
            })
        with open('/tmp/treea.html', 'w') as f:
            f.write('<!DOCTYPE html><html><head><meta charset="utf-8">'
                    '<title>Tree</title></head><body>')
            f.write(string)
            f.write('</body></html>')
