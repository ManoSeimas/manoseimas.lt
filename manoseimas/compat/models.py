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
from sboard.profiles.models import query_group_membership

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


USER_PROFILE, MP_PROFILE, FRACTION_PROFILE, GROUP_PROFILE = range(4)

PROFILE_TYPES = (
    (USER_PROFILE, _('User')),
    (MP_PROFILE, _('Member of Parliament')),
    (FRACTION_PROFILE, _('Fraction')),
    (GROUP_PROFILE, _('Group')),
)


class PersonPositionManager(models.Manager):
    def mps(self, solution_id):
        return self.filter(node=solution_id, profile_type=MP_PROFILE)

    def mp_pairs(self, solution_id, limit=200):
        mps = self.mps(solution_id)
        aye = mps.filter(position__gt=0).order_by('-position')
        against = mps.filter(position__lte=0).order_by('position')
        return (aye[:limit], against[:limit])

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
    position = models.DecimalField(max_digits=7, decimal_places=4, db_index=True)
    participation = models.DecimalField(max_digits=7, decimal_places=4, db_index=True, default=dc(1))

    objects = PersonPositionManager()

    def percent(self):
        return int((abs(self.position) / dc(2)) * dc(100))

    def classify(self):
        if -2 <= self.position < -1.32:
            return _(u'Stipriai prieš')
        elif -1.32 <= self.position < -0.66:
            return _(u'Prieš')
        elif -0.66 <= self.position < 0:
            return _(u'Silpnai prieš')
        elif self.position == 0:
            return _(u'Neutraliai')
        elif 0 < self.position <= 0.66:
            return _(u'Silpnai už')
        elif 0.66 < self.position <= 1.32:
            return _(u'Už')
        else:
            return _(u'Stipriai už')


class Compatibility(object):
    """Represents compatibility between the user and an MP or fraction.

    The compatibility value belongs to the range [-2; 2], with -2 being the least compatible
    (polar opposites)."""

    def __init__(self, profile, profile_type, compatibility, precision):
        self.profile = profile
        self.profile_type = profile_type
        self.compatibility = compatibility
        self.precision = precision

    def percent(self):
        return int((abs(self.compatibility) / dc(2)) * dc(100))

    def precision_percent(self):
        return int(self.precision * dc(100))


def compatibilities(positions, profile_type):
    profile_sums = {}
    for solution_id, position in positions:
        for pp in PersonPosition.objects.filter(node=solution_id, profile_type=profile_type):
            profile_id = pp.profile._id
            ps = profile_sums.setdefault(profile_id, {
                'profile': pp.profile,
                'weighted_positions': 0,
                'weights': 0,
                'participations': 0,
                'total_participation': 0,
            })
            # Note: not exactly a weighted average, because the user's
            # positions can be negative, but the denominator is the sum of
            # their absolute values.
            ps['weighted_positions'] += pp.position * position
            ps['weights'] += abs(position)
            ps['participations'] += pp.participation
            ps['total_participation'] += 1

    for profile_id, sums in profile_sums.items():
        compatibility = dc(sums['weighted_positions']) / dc(sums['weights'])
        precision = dc(sums['participations']) / dc(sums['total_participation'])
        yield Compatibility(
            profile=sums['profile'],
            profile_type=profile_type,
            compatibility=compatibility,
            precision=precision,
        )


def compatibilities_by_sign(positions, profile_type, limit):
    aye, against = [], []

    for compat in compatibilities(positions, profile_type):
        if compat.compatibility > 0:
            aye.append(compat)
        else:
            against.append(compat)

    by_compatibility = lambda c: c.compatibility
    aye.sort(reverse=True, key=by_compatibility)
    against.sort(key=by_compatibility)

    return (aye, against)


def mp_compatibilities_by_sign(positions, limit=200):
    return compatibilities_by_sign(positions, MP_PROFILE, limit)


def fraction_compatibilities_by_sign(positions, limit=200):
    return compatibilities_by_sign(positions, FRACTION_PROFILE, limit)


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
    return (sum, avg)


def calculate_mps_positions(solution_id):
    """Returns dict with position of each MP for this solution.

    Positions are calculated from assigned votings for this solutions.

    """
    mps = {}
    votings_weight = 0.0
    # Loop for all votings
    for voting in query_solution_votings(solution_id):
        voting_weight = voting.solutions[solution_id]
        votings_weight += abs(voting_weight)
        # Loop for all vote values (aye, abstain, no)
        for vote_value_name, votes in voting.votes.items():   # misses 'no-vote' option?
            vote_value = voting.get_vote_value(vote_value_name)
            # Loop for each MP vote
            for mp_id, fraction_id in votes:
                if mp_id not in mps:
                    mps[mp_id] = {
                        'weighted_votes': 0.0,
                        'weight_sum': 0.0,
                    }
                mps[mp_id]['weighted_votes'] += vote_value * voting_weight
                mps[mp_id]['weight_sum'] += abs(voting_weight)
                mps[mp_id]['fraction'] = fraction_id

    fractions = {}
    # Fraction position is calculated as an average of mp positions weighted by
    # their participation, which is the weighted ratio of votings that they
    # have participated in.
    for mp_id, mp in mps.items():
        mp['position'] = mp['weighted_votes'] / mp['weight_sum']
        mp['participation'] = mp['weight_sum'] / votings_weight

        fraction_id = mp['fraction']
        # Some old fractions may not be imported, so we need to check
        # if fraction id is not null.
        #
        # To fix this, some smart importer should be written, that
        # imports all fractions, even old ones, that no longer exists.
        if fraction_id:
            if fraction_id not in fractions:
                fractions[fraction_id] = {
                    'weighted_positions': 0.0,
                    'participation_sum': 0.0,
                }
            fractions[fraction_id]['weighted_positions'] += mp['position'] * mp['participation']
            fractions[fraction_id]['participation_sum'] += mp['participation']

    for fraction_id, fraction in fractions.items():
        fraction['position'] = fraction['weighted_positions'] / fraction['participation_sum']

        mp_count = len(list(query_group_membership(fraction_id)))
        fraction['participation'] = fraction['participation_sum'] / mp_count

    return (fractions, mps)


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
        for profile_id, values in positions.items():
            position = PersonPosition()
            position.node = solution_id
            position.position = values['position']
            position.participation = values['participation']
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


def fetch_user_positions(request, user):
    profile_id = user.get_profile().node._id
    qry = PersonPosition.objects.filter(profile=profile_id)
    for position in qry:
        yield (position.node.ref, position.position)
