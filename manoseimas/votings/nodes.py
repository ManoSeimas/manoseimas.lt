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

import urlparse

from zope.component import adapts
from zope.component import provideAdapter

from django.shortcuts import redirect

from sboard.models import couch
from sboard.nodes import DetailsView

from .interfaces import IVoting


class VotingView(DetailsView):
    adapts(IVoting)

    template = 'votings/voting_details.html'

    def get_related_legal_acts(self):
        return couch.view('legislation/related_legal_acts', key=self.node._id)

    def render(self, **overrides):
        context = {
            'related_legal_acts': self.get_related_legal_acts(),
        }
        context.update(overrides)
        return super(VotingView, self).render(**context)

provideAdapter(VotingView)


def search_lrs_url(query):
    url = urlparse.urlparse(query)
    qry = urlparse.parse_qs(url.query)
    if url.netloc.endswith('.lrs.lt') and 'p_bals_id' in qry:
        try:
            source_id = int(qry['p_bals_id'][0])
        except ValueError:
            source_id = None
        if source_id:
            node = couch.view('votings/by_source_id', key=source_id).first()
            return redirect(node.permalink())
