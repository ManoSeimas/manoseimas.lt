# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import manoseimas.mps_v2.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0017_auto_20150615_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(populate_from=b'name', max_length=120, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='parliamentmember',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(populate_from=('first_name', 'last_name'), max_length=120, editable=False, blank=True),
        ),
    ]
