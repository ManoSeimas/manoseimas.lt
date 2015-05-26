# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import manoseimas.mps_v2.models


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0002_group_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='parliamentmember',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', populate_from=manoseimas.mps_v2.models.get_mp_full_name, editable=False),
            preserve_default=False,
        ),
    ]
