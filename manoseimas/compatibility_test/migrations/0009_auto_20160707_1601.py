# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0008_auto_20160702_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicvoting',
            name='factor',
            field=models.IntegerField(default=1),
        ),
    ]
