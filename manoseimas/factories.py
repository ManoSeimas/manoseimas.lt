# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import factory

from django.conf import settings
from factory.django import DjangoModelFactory


class AdminUserFactory(DjangoModelFactory):
    username = 'admin'
    first_name = 'Admin'
    last_name = ''
    email = factory.LazyAttribute(lambda x: '%s@example.com' % x.username)
    is_active = True
    is_superuser = True
    is_staff = True

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)
