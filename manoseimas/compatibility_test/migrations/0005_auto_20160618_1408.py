# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0004_auto_20160601_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='argument',
            name='topic',
            field=models.ForeignKey(related_name='arguments', to='compatibility_test.Topic'),
        ),
        migrations.AlterField(
            model_name='testgroup',
            name='topics',
            field=models.ManyToManyField(related_name='groups', to='compatibility_test.Topic'),
        ),
    ]
