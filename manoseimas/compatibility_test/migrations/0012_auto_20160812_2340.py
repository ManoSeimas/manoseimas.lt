# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0011_argument_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='argument',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='argument',
            name='short_description',
            field=models.TextField(max_length=300),
        ),
    ]
