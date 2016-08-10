# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import itertools

import factory

from django.conf import settings
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyNaiveDateTime

from manoseimas.scrapy.models import Voting, PersonVote
from manoseimas.mps_v2.factories import GroupFactory, ParliamentMemberFactory, GroupMembershipFactory
from manoseimas.compatibility_test.models import Topic, TopicVoting, CompatTest, TestGroup, Argument, UserResult
from manoseimas.compatibility_test.services import get_topic_positions, update_topic_positions


class UserFactory(DjangoModelFactory):
    first_name = 'Vardenis'
    last_name = 'Pavardenis'
    username = 'vardenis'
    email = factory.LazyAttribute(lambda x: '%s@example.com' % x.username)
    is_active = True

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)


class VotingFactory(DjangoModelFactory):
    key = factory.Sequence(lambda n: '%dv' % n)
    value = {
        'documents': [
            {
                'id': '393905d',
                'type': 'pateikimas',
                'number': 'XIP-2992',
                'name': (
                    'Valstybės saugumo departamento įstatymo 10 straipsnio '
                    'pakeitimo ĮSTATYMO PROJEKTAS (Nr. XIP-2992)'
                )
            },
        ],
    }
    name = 'priėmimas po pateikimo'
    timestamp = FuzzyNaiveDateTime(datetime.datetime(2012, 11, 16))
    source = factory.Sequence(lambda n: 'http://www3.lrs.lt/pls/inter/w5_sale.bals?p_bals_id=%d' % n)

    class Meta:
        model = Voting
        django_get_or_create = ('name',)


class TopicFactory(DjangoModelFactory):
    name = 'Aukštojo mokslo reforma'
    description = 'Aukštojo mokslo reforma'

    class Meta:
        model = Topic
        django_get_or_create = ('name',)


class TopicVotingFactory(DjangoModelFactory):
    topic = factory.SubFactory(TopicFactory)
    voting = factory.SubFactory(VotingFactory)
    factor = 1

    class Meta:
        model = TopicVoting
        django_get_or_create = ('topic', 'voting',)


class CompatTestFactory(DjangoModelFactory):
    name = '2016 election'
    description = ''

    class Meta:
        model = CompatTest
        django_get_or_create = ('name',)


class TestGroupFactory(DjangoModelFactory):
    name = 'Socialiniai reikalai'
    test = factory.SubFactory(CompatTestFactory)

    class Meta:
        model = TestGroup
        django_get_or_create = ('name',)

    @factory.post_generation
    def topics(self, create, extracted, **kwargs):
        if create:
            self.topics = extracted or []


class ArgumentFactory(DjangoModelFactory):
    name = 'Efektyvesnė veikla'
    description = 'Reforma skatina aukštųjų mokyklų jungimąsi, didina jų konkurencingumą, studijų ir mokslo potencialą.'
    supporting = True
    topic = factory.SubFactory(TopicFactory)

    class Meta:
        model = Argument
        django_get_or_create = ('name',)


class UserResultFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    test = factory.SubFactory(CompatTestFactory)
    result = {}

    class Meta:
        model = UserResult
        django_get_or_create = ('user', 'test')


def compatibility_test_factory(term, topic, data):
    votings = []
    seq = itertools.count(1)

    # Create fractions
    groups = {}
    for fraction in set([x[1] for x in data]):
        groups[fraction] = GroupFactory(abbr=fraction, name=fraction)

    # Create some votings and assign them to the topic
    for i in range(3):
        voting = VotingFactory()
        TopicVotingFactory(topic=topic, voting=voting)
        votings.append(voting)

    # Create person votes for topic and votings
    for p_asm_id, fraction, first_name, last_name, votes in data:
        group = groups[fraction]
        mp = ParliamentMemberFactory(
            source_id=p_asm_id,
            first_name=first_name,
            last_name=last_name,
            term_of_office='{0:%Y}-{1:%Y}'.format(*term),
        )
        GroupMembershipFactory(member=mp, group=group)
        for i, vote in enumerate(votes):
            PersonVote.objects.create(
                key=str(next(seq)),
                voting_id=votings[i].key,
                p_asm_id=p_asm_id,
                fraction=fraction,
                name='%s %s' % (first_name, last_name),
                vote=vote,
                timestamp=term.since,
            )

    update_topic_positions(get_topic_positions(term))
