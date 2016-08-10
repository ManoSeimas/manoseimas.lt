# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0006_userresult'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compattest',
            options={'verbose_name': 'Testas', 'verbose_name_plural': 'Testai'},
        ),
        migrations.AlterModelOptions(
            name='testgroup',
            options={'verbose_name': 'Testo grup\u0117', 'verbose_name_plural': 'Testo grup\u0117s'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': 'Tema', 'verbose_name_plural': 'Temos'},
        ),
        migrations.AlterField(
            model_name='compattest',
            name='description',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='positions',
            field=jsonfield.fields.JSONField(default=dict, editable=False),
        ),
    ]
