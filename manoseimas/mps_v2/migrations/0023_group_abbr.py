# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0022_auto_20150616_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='abbr',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
