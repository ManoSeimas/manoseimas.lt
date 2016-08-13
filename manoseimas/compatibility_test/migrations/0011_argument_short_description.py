# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0010_remove_topic_positions'),
    ]

    operations = [
        migrations.AddField(
            model_name='argument',
            name='short_description',
            field=models.TextField(default='No description', max_length=400),
            preserve_default=False,
        ),
    ]
