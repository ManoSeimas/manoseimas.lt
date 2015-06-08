# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0011_group_displayed'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'fraction_logos', blank=True),
        ),
    ]
