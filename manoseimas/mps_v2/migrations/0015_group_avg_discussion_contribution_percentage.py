# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0014_auto_20150612_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='avg_discussion_contribution_percentage',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
