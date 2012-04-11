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
from sboard.models import Node

from .interfaces import ISolution
from .interfaces import IVoting


class Source(schema.DocumentSchema):
    id = schema.IntegerProperty()
    url = schema.StringProperty()


class Voting(Node):
    implements(IVoting)

    # Number of people, that has voting right
    has_voting_right = schema.IntegerProperty()

    # Number of people, that registered for this voting session.
    registered_for_voting = schema.IntegerProperty()

    # Total votes received.
    total_votes = schema.IntegerProperty()

    # Voting results.
    vote_abstain = schema.IntegerProperty()
    vote_aye = schema.IntegerProperty()
    vote_no = schema.IntegerProperty()

    # Voting type (regular, urgent, ...)
    voting_type = schema.StringProperty()

    # List of votes by person and fraction.
    votes = schema.ListProperty()

    # List of legal acts that was directly voted for with this voting.
    legal_acts = schema.ListProperty()

    # List of legal acts that are parents of all legal acts voted for.
    parent_legal_acts = schema.ListProperty()

    # Source of information.
    # FIXME: https://github.com/benoitc/couchdbkit/issues/119
    #source = schema.SchemaDictProperty(Source())
    source = schema.DictProperty()

    def did_not_vote(self):
        """Number of people that registered for voting session, but did not
        vote."""
        return self.registered_for_voting - self.total_votes

provideNode(Voting, "voting")


class Solution(Node):
    implements(ISolution)

provideNode(Solution, "solution")
