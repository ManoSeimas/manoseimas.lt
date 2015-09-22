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

from collections import defaultdict

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from sboard.models import couch
from sboard.nodes import DetailsView

from .interfaces import IVoting
from .models import get_voting_by_lrslt_url
from .models import get_full_voting

from operator import attrgetter

def voting_nav(node, nav, active):
    active = active or ('index',)

    nav.append({
        'key': 'node-title',
        'title': _('Balsavimas'),
        'header': True,
    })

    key = 'index'
    nav.append({
        'key': key,
        'url': node.permalink(),
        'title': _(u'Apžvalga'),
        'children': [],
        'active': key in active,
    })

    key = 'seimo-pozicija'
    nav.append({
        'key': key,
        'url': node.permalink(key),
        'title': _('Seimo pozicija'),
        'children': [],
        'active': key in active,
    })

    return nav

class VotingView(DetailsView):
    adapts(IVoting)

    template = 'votings/voting_details.html'

    def nav(self, active=tuple()):
        nav = super(VotingView, self).nav(active)
        return voting_nav(self.node, nav, active)

    def get_related_legal_acts(self):
        return couch.view('legislation/related_legal_acts', key=self.node._id)

    def render(self, **overrides):
        context = {
            'related_legal_acts': self.get_related_legal_acts(),
        }
        context.update(overrides)
        return super(VotingView, self).render(**context)

provideAdapter(VotingView)

class MPsPositionView(DetailsView):
    adapts(IVoting)
    template = 'votings/mps_position.html'

    def nav(self, active=tuple()):
        active = active or ('seimo-pozicija')
        nav = super(MPsPositionView, self).nav(active)
        return voting_nav(self.node, nav, active)

    def render(self, **overrides):
        voting = get_full_voting(self.node._id)

        fractions_sorted = defaultdict(list)
        mps_sorted = defaultdict(list)

        for fraction in sorted(voting.fractions, key=attrgetter('viso')):
            fractions_sorted[fraction.supports].append(fraction)

        # Sort by highest support
        fractions_sorted[True].reverse()

        for mp in sorted(voting.mps, key=attrgetter('last_name', 'first_name')):
            mps_sorted[ mp.vote ].append(mp)

        context = {
                'fractions': ( fractions_sorted[True], fractions_sorted[False]),
                'mps': ( mps_sorted['aye'], mps_sorted['no'], mps_sorted['abstain'] ),
                'voting': voting
        }
        context.update(overrides)
        return super(MPsPositionView, self).render(**context)

provideAdapter(MPsPositionView, name='seimo-pozicija')


def search_lrs_url(query):
    node = get_voting_by_lrslt_url(query)
    if node:
        return redirect(node.permalink())
