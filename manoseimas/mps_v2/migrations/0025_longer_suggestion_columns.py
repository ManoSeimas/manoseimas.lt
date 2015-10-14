# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0024_add_suggestions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='document',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='opinion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='submitter',
            field=models.TextField(),
        ),
    ]
