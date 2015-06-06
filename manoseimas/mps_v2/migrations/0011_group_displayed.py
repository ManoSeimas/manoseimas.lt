# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0010_auto_20150606_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='displayed',
            field=models.BooleanField(default=True),
        ),
    ]
