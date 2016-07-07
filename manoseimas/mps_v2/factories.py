# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import factory

from django.template.defaultfilters import slugify

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyNaiveDateTime

from manoseimas.mps_v2.models import Group, ParliamentMember, GroupMembership


class ParliamentMemberFactory(DjangoModelFactory):
    slug = factory.LazyAttribute(lambda x: slugify(x.first_name + ' ' + x.last_name))
    source_id = factory.Sequence(lambda n: '%s' % n)
    first_name = 'Petras'
    last_name = 'Gražulis'
    date_of_birth = FuzzyNaiveDateTime(datetime.datetime(1950, 1, 1))
    email = factory.LazyAttribute(lambda x: '%s.%s@lrs.lt' % (x.first_name.lower(), x.last_name.lower()))
    phone = factory.Sequence(lambda n: '+370600%05d' % n)
    photo = factory.django.ImageField()
    positions = {}

    class Meta:
        model = ParliamentMember
        django_get_or_create = ('slug',)


class GroupFactory(DjangoModelFactory):
    slug = factory.LazyAttribute(lambda x: slugify(x.abbr))
    name = 'Lietuvos socialdemokratų partijos frakcija'
    abbr = 'LSDPF'
    type = Group.TYPE_FRACTION
    logo = factory.django.ImageField()

    class Meta:
        model = Group
        django_get_or_create = ('slug',)


class GroupMembershipFactory(DjangoModelFactory):
    member = factory.SubFactory(ParliamentMemberFactory)
    group = factory.SubFactory(GroupFactory)
    since = datetime.datetime(2012, 10, 14)
    until = None

    class Meta:
        model = GroupMembership
