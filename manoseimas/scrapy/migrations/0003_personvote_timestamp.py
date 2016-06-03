# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy', '0002_auto_20160601_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='personvote',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
