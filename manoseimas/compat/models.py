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

from decimal import Decimal as dc

from zope.interface import implements

from django.db import models
from django.utils.translation import ugettext_lazy as _

from couchdbkit.ext.django import schema

from sboard.categories.models import Category
from sboard.factory import provideNode
from sboard.models import NodeForeignKey
from sboard.models import couch
from sboard.models import parse_node_slug

from .interfaces import ICompat



class SolutionCompat(Category):
    implements(ICompat)

    categories = schema.ListProperty()

    def get_solutions(self, category):
        keys = []
        categories = dict(self.categories)
        category = categories.get(category)
        if category:
            for slug in category['solutions']:
                slug, key = parse_node_slug(slug)
                if key:
                    keys.append(key)
            return couch.view('_all_docs', keys=keys)
        else:
            return []

provideNode(SolutionCompat, "solutions-test")


USER_PROFILE = 0
MP_PROFILE = 1
PROFILE_TYPES = (
    (USER_PROFILE, _('User')),
    (USER_PROFILE, _('Memeber of Parlament')),
)

class PersonPositionManager(models.Manager):
    def mps(self, solution_id):
        return self.filter(node=solution_id, profile_type=MP_PROFILE)

    def mp_pairs(self, solution_id, limit=200):
        mps = self.mps(solution_id)
        aye = mps.filter(position__gt=0).order_by('-position')
        against = mps.filter(position__lte=0).order_by('position')
        return (aye[:limit], against[:limit])


class PersonPosition(models.Model):
    node = NodeForeignKey()
    profile = NodeForeignKey()
    profile_type = models.IntegerField(choices=PROFILE_TYPES,
                                       default=USER_PROFILE)
    position = models.DecimalField(max_digits=7, decimal_places=4)

    objects = PersonPositionManager()

    def position_percent(self):
        return int((abs(self.position) / dc(2)) * dc(100))


def query_solution_votings(solution_id):
    return couch.view('solutions/votings', key=solution_id)


def calculate_mps_positions(solution_id):
    """Returns dict with position of each MP for this solution.

    Positions are calculated from assigned votings for this solutions.

    """
    mps = {}
    # Loop for all votings
    for voting in query_solution_votings(solution_id):
        position = voting.solutions[solution_id]
        # Loop for all vote values (aye, abstain, no)
        for vote_value, votes in voting.votes.items():
            vote_value = voting.get_vote_value(vote_value)
            # Loop for each MP vote
            for mp_id, fraction_id in votes:
                if mp_id not in mps:
                    mps[mp_id] = {'times': 0, 'sum': 0}

                mps[mp_id]['times'] += abs(position)
                mps[mp_id]['sum'] += vote_value * position

    return dict([(mp_id, 1.0 * mp['sum'] / mp['times'])
                 for mp_id, mp in mps.items()])


def update_mps_positions(solution_id):
    # Clear MPs positions of solution
    PersonPosition.objects.mps(solution_id).delete()

    # Calculate MPs positions from votings assigned to this solution
    raw_positions = calculate_mps_positions(solution_id)

    # Save calculated positions to PersonPosition table
    for profile_id, value in raw_positions.items():
        position = PersonPosition()
        position.node = solution_id
        position.position = value
        position.profile = profile_id
        position.profile_type = MP_PROFILE
        position.save()
