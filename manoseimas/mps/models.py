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

from couchdbkit.ext.django import schema
from django.core.urlresolvers import reverse

from sboard.factory import provideNode
from sboard.models import NodeProperty
from sboard.models import couch
from sboard.profiles.models import ProfileNode
from sboard.profiles.models import GroupNode
from sboard.profiles.models import query_group_membership

from manoseimas.compat.models import PersonPosition
from manoseimas.compat.models import update_parliament_positions

from .interfaces import ICommission
from .interfaces import ICommittee
from .interfaces import IFraction
from .interfaces import IMPProfile
from .interfaces import IParliament
from .interfaces import IParliamentaryGroup
from .interfaces import IParty
from .interfaces import IPoliticalGroup


class MPProfile(ProfileNode):
    implements(IMPProfile)

    fraction = NodeProperty()

    _default_importance = 9

    def fraction_abbreviation(self):
        if self.fraction:
            return self.fraction.ref.abbreviation

    def permalink(self):
        return reverse('mp_profile', kwargs={'mp_slug': self.slug[:50]})

provideNode(MPProfile, "mpprofile")


class PoliticalGroup(GroupNode):
    implements(IPoliticalGroup)

    source = schema.StringProperty()

    _default_importance = 4


class Fraction(PoliticalGroup):
    implements(IFraction)

    # Reference to a fraction, that this fraction is merged to.
    # All votings done by this fraction goes to merged fraction (if specified).
    mergedto = NodeProperty(required=False)

    abbreviation = schema.StringProperty()

    _default_importance = 6

    def fraction_abbreviation(self):
        return self.abbreviation

    def members(self):
        memberships = query_group_membership(self._id)
        return set(m.profile.ref for m in memberships)

    def permalink(self):
        return reverse('mp_fraction', kwargs={'fraction_slug': self.slug[:120]})

provideNode(Fraction, "fraction")


def query_fractions():
    return couch.view('sboard/by_type', startkey=[Fraction.__name__], endkey=[Fraction.__name__, {}]).iterator()


class Committee(PoliticalGroup):
    implements(ICommittee)

provideNode(Committee, "committee")


class Commission(PoliticalGroup):
    implements(ICommission)

provideNode(Commission, "commission")


class Parliament(PoliticalGroup):
    implements(IParliament)

provideNode(Parliament, "parliament")


class ParliamentaryGroup(PoliticalGroup):
    implements(IParliamentaryGroup)

provideNode(ParliamentaryGroup, 'parliamentarygroup')


class Party(PoliticalGroup):
    implements(IParty)

    _default_importance = 7

provideNode(Party, 'party')


def get_votings_by_fraction_id(fraction_id, **kwargs):
    return couch.view('mps/votings_by_fraction', key=fraction_id, **kwargs)


def merge_fraction_votings(source, dest):
    votings = set()
    for voting in get_votings_by_fraction_id(source.key):
        for votes in voting.votes.values():
            for i, (mp_vote, fraction_vote) in enumerate(votes):
                if fraction_vote == source.key:
                    votes[i][1] = dest.key
        voting.save()
        votings.add(voting.key)

    votings = list(votings)
    solutions = couch.view('votings/solutions_by_voting', keys=votings)
    solutions = set([solution.key for solution in solutions])
    for solution_id in solutions:
        PersonPosition.objects.filter(node=solution_id).delete()
        update_parliament_positions(solution_id)
