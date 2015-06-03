# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0003_auto_20150602_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='stenogramstatement',
            name='word_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
