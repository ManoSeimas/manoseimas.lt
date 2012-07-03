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

import operator

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

    def default_category(self):
        if self.categories:
            return self.categories[0][0]

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
FRACTION_PROFILE = 2
GROUP_PROFILE = 3
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

    def mp_compat_pairs(self, positions, limit=200):
        mps = {}
        for solution_id, position in positions:
            for mp in self.mps(solution_id):
                mpid = mp.profile._id
                sum, count = mps.get(mpid, (0, 0))
                sum += mp.position * position
                mps[mpid] = (sum, count + abs(position))

        aye, against = [], []
        for mpid, numbers in mps.items():
            sum, count = numbers
            avg = dc(sum) / dc(count)
            if avg > 0:
                aye.append((mpid, avg))
            else:
                against.append((mpid, avg))

        aye = sorted(aye, key=operator.itemgetter(1), reverse=True)
        against = sorted(against, key=operator.itemgetter(1))

        results = ([], [])
        for i, mps in enumerate((aye, against)):
            for mpid, avg in mps[:limit]:
                position = PersonPosition()
                position.profile = mpid
                position.profile_type = MP_PROFILE
                position.position = avg
                results[i].append(position)

        return results

    def fractions(self, solution_id):
        return self.filter(node=solution_id, profile_type=FRACTION_PROFILE)

    def fraction_pairs(self, solution_id, limit=200):
        fractions = self.fractions(solution_id)
        aye = fractions.filter(position__gt=0).order_by('-position')
        against = fractions.filter(position__lte=0).order_by('position')
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
    for node in couch.view('solutions/votings', key=solution_id):
        node.weight = node.solutions[solution_id]   # how the voting influences solution
        node.weight_plus_if_needed = "+" if node.weight > 0 else ""

        # was voting "accepted" - ar istatymas buvo priimtas? 
        # TODO: https://bitbucket.org/manoseimas/manoseimas/issue/88/i-lrs-svetain-s-nusiurbti-info-ar

        # calculate general parliament position as one number

        node.avg_parl_position_normalized = sum([
            node.vote_aye * node.get_vote_value('aye'),
            node.vote_no * node.get_vote_value('no'),
            node.vote_abstain * node.get_vote_value('abstain'),
            node.did_not_vote() * node.get_vote_value('no-vote'),
        ]) / dc(node.registered_for_voting) / dc(2)  # normalize (divide by max amplitude -- 2)
        node.weighted_avg_parl_position = node.weight * node.avg_parl_position_normalized
        yield node


def calculate_solution_parliament_avg_position(solution_id):
    sum, items = 0, 0
    for voting in query_solution_votings(solution_id):
        sum += voting.weight * voting.avg_parl_position_normalized
        items += abs(voting.weight)
    avg = sum / dc(items)
    return (sum,  avg)


def calculate_mps_positions(solution_id):
    """Returns dict with position of each MP for this solution.

    Positions are calculated from assigned votings for this solutions.

    """
    mps = {}
    fractions = {}
    # Loop for all votings
    for voting in query_solution_votings(solution_id):
        voting_weight = voting.solutions[solution_id]
        # Loop for all vote values (aye, abstain, no)
        for vote_value_name, votes in voting.votes.items():   # misses 'no-vote' option?
            vote_value = voting.get_vote_value(vote_value_name)
            # Loop for each MP vote
            for mp_id, fraction_id in votes:
                if mp_id not in mps:
                    mps[mp_id] = {'times': 0, 'sum': 0}
                mps[mp_id]['times'] += abs(voting_weight)
                mps[mp_id]['sum'] += vote_value * voting_weight

                # Some old fractions may not be imported, so we need to check
                # if fraction id is not null.
                #
                # To fix this, some smart importer should be written, that
                # imports all fractions, even old ones, that no longer exists.
                if fraction_id:
                    if fraction_id not in fractions:
                        fractions[fraction_id] = {'times': 0, 'sum': 0}
                    fractions[fraction_id]['times'] += abs(voting_weight)
                    fractions[fraction_id]['sum'] += vote_value * voting_weight

    return (
        dict([(fraction_id, 1.0 * fraction['sum'] / fraction['times'])
                 for fraction_id, fraction in fractions.items()]),
        dict([(mp_id, 1.0 * mp['sum'] / mp['times'])
                 for mp_id, mp in mps.items()])
    )


def update_mps_positions(solution_id):
    # Calculate MPs positions from votings assigned to this solution
    fractions, mps = calculate_mps_positions(solution_id)

    items = (
        (
            PersonPosition.objects.fractions,
            fractions,
            FRACTION_PROFILE,
        ),
        (
            PersonPosition.objects.mps,
            mps,
            MP_PROFILE,
        ),
    )

    for qry, positions, profile_type in items:
        # Clear positions of solution
        qry(solution_id).delete()

        # Save calculated positions to PersonPosition table
        for profile_id, value in positions.items():
            position = PersonPosition()
            position.node = solution_id
            position.position = value
            position.profile = profile_id
            position.profile_type = profile_type
            position.save()


def update_anonymous_position(request, solution_id, value):
    if 'positions' not in request.session:
        request.session['positions'] = {}
    request.session['positions'][solution_id] = value
    request.session.modified = True


def update_user_position(user, solution_id, value):
    profile = user.get_profile().node

    params = dict(node=solution_id, profile=profile._id)
    try:
        position = PersonPosition.objects.get(**params)
    except PersonPosition.DoesNotExist:
        position = PersonPosition(**params)
        position.profile_type = USER_PROFILE

    if value:
        position.position = value
        position.save()
    elif position.pk:
        position.delete()


def update_position(request, solution_id, value):
    if request.user.is_anonymous():
        update_anonymous_position(request, solution_id, value)
    else:
        update_user_position(request.user, solution_id, value)


def query_positions(request):
    if request.user.is_anonymous():
        return request.session.get('positions', {}).items()
    else:
        profile_id = request.user.get_profile().node._id
        qry = PersonPosition.objects.filter(profile=profile_id)
        return ((p.node._id, p.position) for p in qry)


def anonymous_positions_map(request):
    return request.session.get('positions', {})


def user_positions_map(user, nodes):
    keys = []
    node_map = {}
    for node in nodes:
        key = node._id
        keys.append(key)
        node_map[key] = node

    positions = {}
    profile_id = user.get_profile().node._id
    qry = PersonPosition.objects.filter(profile=profile_id, node__in=keys)
    for position in qry:
        node = node_map[position.node._id]
        positions[node._id] = position.position

    return positions


def fetch_positions(request, nodes):
    if request.user.is_anonymous():
        positions = anonymous_positions_map(request)
    else:
        positions = user_positions_map(request.user, nodes)
    for node in nodes:
        position = positions.get(node._id)
        yield (node, position)
