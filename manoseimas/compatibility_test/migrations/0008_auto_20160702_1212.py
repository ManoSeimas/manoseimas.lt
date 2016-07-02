# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0007_auto_20160622_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testgroup',
            options={'ordering': ('test', 'name'), 'verbose_name': 'Testo grup\u0117', 'verbose_name_plural': 'Testo grup\u0117s'},
        ),
        migrations.AlterField(
            model_name='testgroup',
            name='test',
            field=models.ForeignKey(related_name='groups', to='compatibility_test.CompatTest', null=True),
        ),
        migrations.AlterField(
            model_name='testgroup',
            name='topics',
            field=models.ManyToManyField(related_name='groups', to='compatibility_test.Topic', blank=True),
        ),
    ]
