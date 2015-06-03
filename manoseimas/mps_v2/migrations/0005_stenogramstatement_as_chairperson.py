# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0004_stenogramstatement_word_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='stenogramstatement',
            name='as_chairperson',
            field=models.BooleanField(default=False),
        ),
    ]
