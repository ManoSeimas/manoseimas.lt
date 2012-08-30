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

from sboard.factory import provideNode
from sboard.models import NodeProperty
from sboard.profiles.models import ProfileNode
from sboard.profiles.models import GroupNode
from sboard.profiles.models import query_group_membership

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

provideNode(MPProfile, "mpprofile")


class PoliticalGroup(GroupNode):
    implements(IPoliticalGroup)

    source = schema.StringProperty()

    _default_importance = 4


class Fraction(PoliticalGroup):
    implements(IFraction)

    abbreviation = schema.StringProperty()

    _default_importance = 6

    def fraction_abbreviation(self):
        return self.abbreviation

    def members(self):
        memberships = query_group_membership(self._id)
        return set(m.profile.ref for m in memberships)

provideNode(Fraction, "fraction")


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
