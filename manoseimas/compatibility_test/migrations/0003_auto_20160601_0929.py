# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0002_auto_20160531_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='voting',
            name='documents',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='topic',
            name='mp_positions',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
