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

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.inclusion_tag('manoseimas/legislation/templatetags/menu.html',
                        takes_context=True)
def legislation_menu(context):
    legislation_number = context['legislation'].number
    urls = [
        ('legislation', _(u'Įstatymas'),
         reverse('manoseimas-legislation', args=[legislation_number])),

        ('amendments', _(u'Pataisos'),
         reverse('manoseimas-legislation-amendments',
                 args=[legislation_number])),

        ('drafts', _(u'Projektai'), '#'),
    ]

    active = context.get('legislation_active_page', 'legislation')
    menu = []
    for key, title, url in urls:
        item = {
            'url': url,
            'title': title,
            'is_active': key == active,
        }
        menu.append(item)

    return {
        'legislation_menu': menu,
    }
