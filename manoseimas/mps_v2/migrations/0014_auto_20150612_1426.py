# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0013_stenogram_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='avg_long_statement_count',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='avg_statement_count',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='avg_vote_percentage',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='discussion_contribution_percentage',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='long_statement_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='statement_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='vote_percentage',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
