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

import itertools
from decimal import Decimal as dc
from collections import Counter
from collections import defaultdict

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

from manoseimas.solutions.models import query_solution_votings

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


PARTICIPATION_SHOW_TRESHOLD = 0.1
PARTICIPATION_ACTIVE_TRESHOLD = 0.33


class PersonPositionManager(models.Manager):
    show_q = models.Q(participation__gte=PARTICIPATION_SHOW_TRESHOLD)
    active_q = models.Q(participation__gte=PARTICIPATION_ACTIVE_TRESHOLD)

    def mps(self, solution_id):
        return self.filter(node=solution_id, profile_type=MP_PROFILE)

    def mp_pairs(self, solution_id, limit=200):
        mps = self.mps(solution_id).filter(PersonPositionManager.show_q)

        aye = mps.filter(position__gt=0)
        aye_active = aye.filter(PersonPositionManager.active_q).order_by('-position')[:limit]
        aye_inactive = aye.filter(~PersonPositionManager.active_q).order_by('-participation')[:limit]
        aye_sorted = itertools.chain(aye_active, aye_inactive)

        against = mps.filter(position__lte=0)
        against_active = against.filter(PersonPositionManager.active_q).order_by('position')[:limit]
        against_inactive = against.filter(~PersonPositionManager.active_q).order_by('-participation')[:limit]
        against_sorted = itertools.chain(against_active, against_inactive)

        return (aye_sorted, against_sorted)

    def fractions(self, solution_id):
        return self.filter(node=solution_id, profile_type=FRACTION_PROFILE)

    def fraction_pairs(self, solution_id, limit=200):
        fractions = self.fractions(solution_id).filter(PersonPositionManager.show_q)

        aye = fractions.filter(position__gt=0)
        aye_active = aye.filter(PersonPositionManager.active_q).order_by('-position')[:limit]
        aye_inactive = aye.filter(~PersonPositionManager.active_q).order_by('-participation')[:limit]
        aye_sorted = itertools.chain(aye_active, aye_inactive)

        against = fractions.filter(position__lte=0)
        against_active = against.filter(PersonPositionManager.active_q).order_by('position')[:limit]
        against_inactive = against.filter(~PersonPositionManager.active_q).order_by('-participation')[:limit]
        against_sorted = itertools.chain(against_active, against_inactive)

        return (aye_sorted, against_sorted)


class PersonPosition(models.Model):
    node = NodeForeignKey()
    profile = NodeForeignKey()
    profile_type = models.IntegerField(choices=PROFILE_TYPES,
                                       default=USER_PROFILE)
    position = models.DecimalField(max_digits=7, decimal_places=4, db_index=True)
    participation = models.DecimalField(max_digits=7, decimal_places=4, db_index=True, default=dc(1))

    objects = PersonPositionManager()

    def position_percent(self):
        return int((abs(self.position) / dc(2)) * dc(100))

    def participation_percent(self):
        return int(self.participation * dc(100))

    def classify(self):
        if self.position == 0:
            return _(u'neutraliai')

        if self.positive():
            sign = _(u'už')
        else:
            sign = _(u'prieš')

        percent = self.position_percent()
        if 0 < percent <= 33:
            quantifier = _(u'nestipriai')
        elif 33 < percent <= 66:
            quantifier = _(u'vidutiniškai')
        else:
            quantifier = _(u'stipriai')

        return u'%s %s' % (quantifier, sign)

    def active(self):
        return self.participation >= PARTICIPATION_ACTIVE_TRESHOLD

    def positive(self):
        return self.position > 0

    def __key__(self):
        if self.active():
            second_key = 0
        else:
            second_key = self.participation

        return (self.active(), second_key, abs(self.position))


# Results with lower precision get hidden.
PRECISION_SHOW_TRESHOLD = 0.1

# Results with lower precision get grayed out.
PRECISION_PRECISE_TRESHOLD = 0.33


class Compatibility(object):
    """Represents compatibility between the user and an MP or fraction.

    The compatibility value belongs to the range [-2; 2], with -2 being the least compatible
    (polar opposites)."""

    def __init__(self, profile, profile_type, compatibility, precision):
        self.profile = profile
        self.profile_type = profile_type
        self.compatibility = compatibility
        self.precision = precision

    def compatibility_percent(self):
        return int(abs(self.compatibility) / 2 * 100)

    def precision_percent(self):
        return int(self.precision * 100)

    def precise(self):
        return self.precision > PRECISION_PRECISE_TRESHOLD

    def positive(self):
        return self.compatibility > 0

    def __key__(self):
        # Sort imprecise results by precision instead of compatibility.
        if self.precise():
            second_key = 0
        else:
            second_key = self.precision

        return (self.precise(), second_key, abs(self.compatibility))


def compatibilities(positions, profile_type):
    profile_sums = defaultdict(lambda: Counter())
    user_solutions = 0
    for solution_id, position in positions:
        position = float(position)
        user_solutions += 1
        for pp in PersonPosition.objects.filter(node=solution_id, profile_type=profile_type):
            profile_id = pp.profile._id
            ps = profile_sums[profile_id]
            ps['profile'] = pp.profile
            # Note: not exactly a weighted average, because the user's
            # positions can be negative, but the denominator is the sum of
            # their absolute values.
            ps['weighted_positions'] += float(pp.position) * position
            ps['weights'] += abs(position)
            ps['participation'] += float(pp.participation)

    for profile_id, sums in profile_sums.items():
        precision = sums['participation'] / user_solutions
        if precision > PRECISION_SHOW_TRESHOLD:
            compatibility = sums['weighted_positions'] / sums['weights']
            yield Compatibility(
                profile=sums['profile'],
                profile_type=profile_type,
                compatibility=compatibility,
                precision=precision,
            )


def compatibilities_by_sign(positions, profile_type, precise=False):
    aye, against = [], []

    if precise:
        precisep = lambda c: c.precise()
    else:
        precisep = lambda c: True

    for compat in compatibilities(positions, profile_type):
        if precisep(compat):
            if compat.positive():
                aye.append(compat)
            else:
                against.append(compat)

    aye.sort(reverse=True, key=Compatibility.__key__)
    against.sort(reverse=True, key=Compatibility.__key__)

    return (aye, against)


def mp_compatibilities_by_sign(positions, precise=False):
    return compatibilities_by_sign(positions, MP_PROFILE, precise)


def fraction_compatibilities_by_sign(positions, precise=False):
    return compatibilities_by_sign(positions, FRACTION_PROFILE, precise)


def calculate_solution_parliament_avg_position(solution_id):
    sum, items = 0, 0
    for voting in query_solution_votings(solution_id):
        sum += voting.weight * voting.avg_parl_position_normalized
        items += abs(voting.weight)
    if items:
        avg = sum / dc(items)
    else:
        avg = None
    return (sum, avg)


def calculate_parliament_positions(solution_id):
    mps = defaultdict(lambda: Counter())
    voting_weights_sum = 0
    # Loop for all votings
    for voting in query_solution_votings(solution_id):
        voting_weight = voting.solutions[solution_id]
        voting_weights_sum += abs(voting_weight)
        # Loop for all vote values (aye, abstain, no)
        for vote_value_name, votes in voting.votes.items():
            vote_value = voting.get_vote_value(vote_value_name)
            # Loop for each MP vote
            for mp_id, fraction_id in votes:
                mp = mps[(mp_id, fraction_id)]
                mp['weighted_votes'] += vote_value * voting_weight
                mp['weights'] += abs(voting_weight)

    fractions = defaultdict(lambda: Counter())
    # Fraction position is calculated as an average of mp positions weighted by
    # their participation, which is the weighted ratio of votings that they
    # have participated in.
    for (mp_id, fraction_id), mp in mps.items():
        mp['position'] = mp['weighted_votes'] / float(mp['weights'])
        mp['participation'] = mp['weights'] / float(voting_weights_sum)

        # Some old fractions may not be imported, so we need to check
        # if fraction id is not null.
        #
        # To fix this, the importer should be modified to import fractions
        # which no longer exist.
        if fraction_id:
            fraction = fractions[fraction_id]
            fraction['weighted_positions'] += mp['position'] * mp['participation']
            fraction['participation_sum'] += mp['participation']

    for fraction_id, fraction in fractions.items():
        fraction['position'] = fraction['weighted_positions'] / fraction['participation_sum']

        mp_count = len(list(query_group_membership(fraction_id)))
        fraction['participation'] = fraction['participation_sum'] / mp_count

    return (fractions, {mp_id: mp for (mp_id, fraction_id), mp in mps.items()})


def clear_parliament_positions():
    """Deletes all positions of MPs and Fractions.

    Should be used before regenerating positions for each solution with
    update_parliament_positions. If any solutions were deleted, their positions
    are deleted too this way."""

    PersonPosition.objects.filter(profile_type__in=[MP_PROFILE, FRACTION_PROFILE]).delete()


def update_parliament_positions(solution_id):
    fractions, mps = calculate_parliament_positions(solution_id)

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
