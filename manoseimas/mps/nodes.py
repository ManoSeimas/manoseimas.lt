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

from operator import attrgetter

from zope.component import adapts
from zope.component import provideAdapter

from sboard.nodes import UpdateView
from sboard.profiles.nodes import ProfileView
from sboard.profiles.nodes import GroupView

from django.utils.translation import ugettext as _

from manoseimas.compat.models import PersonPosition

from .interfaces import IMPProfile
from .interfaces import IFraction

from .models import query_fractions

from .forms import FractionForm


def search_lrs_url(query):
    pass


def format_position_percent(personposition):
    if personposition.position >= 0:
        return _(u'Palaiko %d%%') % personposition.position_percent()
    else:
        return _(u'Nepalaiko %d%%') % personposition.position_percent()


def prepare_position_list(node):
    """Returns list of positions of a person or fraction to be passed to a
    template."""
    positions = list(PersonPosition.objects.filter(profile=node))
    positions.sort(key=lambda pp: pp.node.ref.title)
    return [{
        'solution': pp.node,
        'position': pp.classify,
        'percent': format_position_percent(pp),
    } for pp in positions]


class MPProfileView(ProfileView):
    adapts(IMPProfile)
    template = 'mps/profile.html'

    def nav(self, active=tuple()):
        nav = super(MPProfileView, self).nav(active)

        if self.node.fraction:
            nav.append({
                'title': _('Frakcijos nariai'),
                'header': True,
            })

            MEMBER_LIMIT = 10

            members = list(self.node.fraction.ref.members())
            members.sort(key=attrgetter('last_name', 'first_name'))
            for member in members[:MEMBER_LIMIT]:
                nav.append({
                    'title': member.title,
                    'url': member.permalink(),
                    'active': member == self.node,
                })
            if len(members) > MEMBER_LIMIT:
                nav.append({
                    'title': _(u'Daugiau narių…'),
                    'url': self.node.fraction.ref.permalink() + '#nariai',
                })

        return nav

    def render(self, **overrides):
        context = {
            'positions': prepare_position_list(self.node),
        }
        context.update(overrides)
        return super(MPProfileView, self).render(**context)

provideAdapter(MPProfileView)


class FractionView(GroupView):
    adapts(IFraction)
    template = 'mps/fraction.html'

    def nav(self, active=tuple()):
        nav = super(FractionView, self).nav(active)

        nav.append({
            'title': _('Frakcijos'),
            'header': True,
        })

        fractions = sorted(query_fractions(), key=attrgetter('title'))
        for fraction in fractions:
            nav.append({
                'title': fraction.title,
                'url': fraction.permalink(),
                'active': fraction == self.node,
            })

        return nav

    def render(self, **overrides):
        context = {
            'members': sorted(self.node.members(), key=attrgetter('last_name', 'first_name')),
            'positions': prepare_position_list(self.node),
        }
        context.update(overrides)
        return super(FractionView, self).render(**context)

provideAdapter(FractionView)


class FractionUpdateView(UpdateView):
    adapts(IFraction)

    form = FractionForm

provideAdapter(FractionUpdateView, name='update')
