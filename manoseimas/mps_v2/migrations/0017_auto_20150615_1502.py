# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0016_stenogramtopic_presenters'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='positions',
            field=jsonfield.fields.JSONField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='positions',
            field=jsonfield.fields.JSONField(default=None, null=True, blank=True),
        ),
    ]
