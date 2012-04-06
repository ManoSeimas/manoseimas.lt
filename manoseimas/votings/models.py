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
