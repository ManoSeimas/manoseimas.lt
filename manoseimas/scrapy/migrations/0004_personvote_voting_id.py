# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy', '0003_personvote_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='personvote',
            name='voting_id',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
    ]
