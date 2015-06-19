# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0020_lawproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='avg_law_project_count',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='avg_passed_law_project_count',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='avg_passed_law_project_ratio',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='passed_law_project_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='passed_law_project_ratio',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='proposed_law_project_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
