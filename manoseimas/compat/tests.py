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

from mock import Mock

from django.test.client import RequestFactory

from .forms import AssignSolutionsForm
from .forms import CompatNodeForm
from .models import SolutionCompat


class TestCompatNodeForm(unittest.TestCase):
    def setUp(self):
        self.browser = RequestFactory()

    def testSolutions(self):
        node = SolutionCompat()
        node.get_body = Mock(return_value='')

        # If node.categories is empty.
        form = CompatNodeForm(node, {
            'title': 'test',
            'categories': 'a\nb\nc\n',
        })
        is_valid = form.is_valid()
        self.assertTrue(is_valid)

        expected = [
            ['a', {'title': 'a', 'solutions': []}],
            ['b', {'title': 'b', 'solutions': []}],
            ['c', {'title': 'c', 'solutions': []}],
        ]
        self.assertEqual(form.cleaned_data['categories'], expected)

        # Assign solutions to a category.
        node.categories = form.cleaned_data['categories']
        form = AssignSolutionsForm('a', node, {
            'title': 'x',
            'solutions': 's1\ns2\n',
        })
        form.get_node_slug_with_key = Mock(side_effect=['+s1', '+s2'])
        is_valid = form.is_valid()
        self.assertTrue(is_valid)

        expected = [
            ['x', {'title': 'x', 'solutions': ['+s1', '+s2']}],
            ['b', {'title': 'b', 'solutions': []}],
            ['c', {'title': 'c', 'solutions': []}],
        ]
        self.assertEqual(form.cleaned_data['categories'], expected)

        # If node.categories aready has a value (changing order, preserving
        # assigned solutions to existing categories)
        node.categories = form.cleaned_data['categories']
        form = CompatNodeForm(node, {
            'title': 'test',
            'categories': 'b\nx\nc\na\n',
        })
        is_valid = form.is_valid()
        self.assertTrue(is_valid)

        expected = [
            ['b', {'title': 'b', 'solutions': []}],
            ['x', {'title': 'x', 'solutions': ['+s1', '+s2']}],
            ['c', {'title': 'c', 'solutions': []}],
            ['a', {'title': 'a', 'solutions': []}],
        ]
        self.assertEqual(form.cleaned_data['categories'], expected)
