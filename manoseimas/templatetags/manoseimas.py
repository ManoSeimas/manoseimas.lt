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

import re
import unidecode

from django import template
from django.forms.fields import CheckboxInput
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

@register.filter(name='age_plural')
def age_plural(age):
    if age % 10 == 0 or 10 < age < 20:
        return _(u'metų')
    else:
        return _(u'metai')

@register.filter(name='parse_int')
def extract_int(value):
    m = re.search('^(\d+)', value)
    if m:
        return m.group(1)
    else:
        return -1

def normalize_search(value):
    r = unidecode.unidecode(value)
    return r.lower()

@register.filter(name='matching_documents')
def matching_documents(values, query):
    query = normalize_search(query)

    result = "<ul>"
    for doc in values:
        name = normalize_search(doc['name'])
        if query in normalize_search(doc['name']):
            result += "<li>%s</li>" % doc['name']

    result += "</ul>"
    return mark_safe(result)
