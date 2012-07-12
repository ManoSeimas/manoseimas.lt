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

from zope.component import adapts
from zope.component import provideAdapter
from sboard.profiles.nodes import ProfileView
from sboard.profiles.nodes import GroupView
from django.utils.translation import ugettext as _
from manoseimas.compat.models import PersonPosition

from .interfaces import IMPProfile
from .interfaces import IFraction


def search_lrs_url(query):
    pass


def classify_position(position):
    if -2 <= position < -1:
        return _(u'Stipriai prieš')
    elif -1 <= position <= 0:
        return _(u'Prieš')
    elif 0 < position <= 1:
        return _(u'Už')
    else:
        return _(u'Stipriai už')


def format_position_percent(personposition):
    if personposition.position >= 0:
        return _(u'Palaiko %d%%') % personposition.position_percent()
    else:
        return _(u'Nepalaiko %d%%') % personposition.position_percent()


class MPProfileView(ProfileView):
    adapts(IMPProfile)
    template = 'mps/profile.html'

    def render(self, **overrides):
        positions = PersonPosition.objects.filter(profile=self.node)
        context = {
            'positions': [{
                'solution': pp.node,
                'position': classify_position(pp.position),
                'percent': format_position_percent(pp),
            } for pp in positions],
        }
        context.update(overrides)
        return super(MPProfileView, self).render(**context)

provideAdapter(MPProfileView)


class FractionView(GroupView):
    adapts(IFraction)
    template = 'mps/fraction.html'

    def render(self, **overrides):
        positions = PersonPosition.objects.filter(profile=self.node)
        context = {
            'positions': [{
                'solution': pp.node,
                'position': classify_position(pp.position),
                'percent': format_position_percent(pp),
            } for pp in positions],
        }
        context.update(overrides)
        return super(FractionView, self).render(**context)

provideAdapter(FractionView)
