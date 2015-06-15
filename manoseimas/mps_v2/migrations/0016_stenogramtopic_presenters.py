# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0015_group_avg_discussion_contribution_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='stenogramtopic',
            name='presenters',
            field=models.ManyToManyField(related_name='presented_topics', to='mps_v2.ParliamentMember'),
        ),
    ]
