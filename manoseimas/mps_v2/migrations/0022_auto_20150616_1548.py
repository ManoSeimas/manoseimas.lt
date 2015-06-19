# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0021_auto_20150616_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupranking',
            name='passed_law_project_ratio_rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mpranking',
            name='passed_law_project_ratio_rank',
            field=models.IntegerField(default=0),
        ),
    ]
