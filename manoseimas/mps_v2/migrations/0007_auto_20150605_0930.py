# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0006_auto_20150604_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parliamentmember',
            name='groups',
            field=models.ManyToManyField(related_name='members', through='mps_v2.GroupMembership', to='mps_v2.Group'),
        ),
    ]
