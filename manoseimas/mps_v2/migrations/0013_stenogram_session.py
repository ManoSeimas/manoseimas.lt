# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0012_group_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='stenogram',
            name='session',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
