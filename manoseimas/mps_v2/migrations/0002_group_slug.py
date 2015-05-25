# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', populate_from=b'name', editable=False),
            preserve_default=False,
        ),
    ]
