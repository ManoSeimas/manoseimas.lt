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

from zope.interface import implements

from sboard.categories.models import Category
from sboard.factory import provideNode

from couchdbkit.ext.django import schema

from sboard.models import couch
from sboard.models import parse_node_slug

from .interfaces import ICompat


class SolutionCompat(Category):
    implements(ICompat)

    categories = schema.ListProperty()

    def get_solutions(self, category):
        keys = []
        categories = dict(self.categories)
        category = categories.get(category)
        if category:
            for slug in category['solutions']:
                slug, key = parse_node_slug(slug)
                if key:
                    keys.append(key)
            return couch.view('_all_docs', keys=keys)
        else:
            return []

provideNode(SolutionCompat, "solutions-test")
