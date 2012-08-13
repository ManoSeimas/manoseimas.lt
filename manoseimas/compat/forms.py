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

from django import forms
from django.utils.translation import ugettext_lazy as _

from sboard.fields import NodeField
from sboard.forms import BaseNodeForm
from sboard.models import get_node_by_slug
from sboard.utils import slugify


class CompatNodeForm(BaseNodeForm):
    title = forms.CharField()
    categories = forms.Field(widget=forms.Textarea,
            help_text="Enter category names, one category name per line.")

    def get_current_categories(self):
        if self.node:
            try:
                return dict(self.node.categories)
            except ValueError:
                pass
        return dict()

    def get_initial_values(self):
        initial = super(CompatNodeForm, self).get_initial_values()
        if self.node and self.node.categories:
            categories = [c['title'] for slug, c in self.node.categories]
            initial['categories'] = '\n'.join(categories)
        return initial

    def clean_categories(self):
        value = self.cleaned_data.get('categories')
        if value:
            categories = self.get_current_categories()
            cleaned_value = []
            for name in filter(None, value.splitlines()):
                slug = slugify(name)
                if slug in categories:
                    solutions = categories[slug]['solutions']
                else:
                    solutions = []
                item = [slug, {'title': name, 'solutions': solutions}]
                cleaned_value.append(item)
            value = cleaned_value
        return value


class AssignSolutionsForm(BaseNodeForm):
    title = forms.CharField(label=_('Test category title.'))
    solutions = forms.Field(widget=forms.Textarea,
            help_text=_('Enter one solution slug per line.'))

    def __init__(self, category, *args, **kwargs):
        self.category = category
        super(AssignSolutionsForm, self).__init__(*args, **kwargs)

    def get_initial_values(self):
        initial = super(AssignSolutionsForm, self).get_initial_values()
        initial['title'] = ''
        initial['solutions'] = ''
        if self.node and self.node.categories:
            categories = dict(self.node.categories)
            if self.category in categories:
                category = categories[self.category]
                initial['title'] = category['title']
                initial['solutions'] = '\n'.join(category['solutions'])
        return initial

    def get_node_slug_with_key(self, slug):
        if slug:
            node = get_node_by_slug(slug)
            if node:
                return node.get_slug_with_key()
        return None

    def clean_solutions(self):
        value = self.cleaned_data.get('solutions')
        if value:
            solutions = []
            for slug in value.splitlines():
                slug = slug.strip()
                slug = self.get_node_slug_with_key(slug)
                if slug:
                    solutions.append(slug)
            return solutions
        else:
            return []

    def clean(self):
        title = self.cleaned_data.get('title')
        solutions = self.cleaned_data.get('solutions')
        if title and solutions is not None:
            updated = False
            categories = []
            current_categories = []
            if self.node and self.node.categories:
                current_categories = self.node.categories
            for slug, category in current_categories:
                if slug == self.category:
                    slug = slugify(title)
                    category['title'] = title
                    category['solutions'] = solutions
                    updated = True
                categories.append([slug, category])

            if not updated:
                slug = slugify(title)
                category = {
                    'title': title,
                    'solutions': solutions,
                }
                categories.append([slug, category])

        else:
            categories = None

        return {'categories': categories}


class UserPositionForm(forms.Form):
    node = NodeField()
    position = forms.IntegerField(min_value=-2, max_value=2)
