# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0025_longer_suggestion_columns'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='suggestion',
            name='submitter',
        ),
        migrations.AddField(
            model_name='suggestion',
            name='submitter',
            field=models.ManyToManyField(related_name='suggestions', to='mps_v2.Suggester'),
        ),
    ]
