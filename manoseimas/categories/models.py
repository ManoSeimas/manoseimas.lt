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

from couchdbkit.ext.django import schema


def _get_tree_node(row, last_level, current_level, next_level):
    row['open_levels'] = row['close_levels'] = []
    if current_level > last_level:
        row['open_levels'] = range(current_level - last_level)
    if current_level > next_level:
        row['close_levels'] = range(current_level - next_level)
    row['level'] = current_level
    return row


def iterate_tree(view):
    last_level = 0
    current_row = None
    for next_row in view:
        if current_row:
            current_level = len(current_row['key'])
            next_level = len(next_row['key'])
            yield _get_tree_node(current_row, last_level, current_level,
                                 next_level)
            last_level = current_level
        current_row = next_row
    if current_row:
        current_level = len(current_row['key'])
        next_level = 0
        yield _get_tree_node(current_row, last_level, current_level,
                             next_level)


class Category(schema.Document):
    @classmethod
    def get_tree(cls):
        view = cls.get_db().view('categories/tree', include_docs=True)
        #view = cls.view('categories/tree', include_docs=True)
        return iterate_tree(view)
