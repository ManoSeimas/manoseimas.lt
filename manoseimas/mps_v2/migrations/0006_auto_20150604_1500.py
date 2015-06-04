# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0005_stenogramstatement_as_chairperson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parliamentmember',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'profile_images', blank=True),
        ),
    ]
