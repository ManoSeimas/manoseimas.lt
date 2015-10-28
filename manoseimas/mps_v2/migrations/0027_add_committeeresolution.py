# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0026_auto_20151027_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeResolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('source_id', models.CharField(unique=True, max_length=16)),
                ('title', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
