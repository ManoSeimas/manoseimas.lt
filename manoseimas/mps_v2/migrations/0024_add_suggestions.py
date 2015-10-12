# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0023_group_abbr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('source_id', models.CharField(max_length=16, db_index=True)),
                ('source_index', models.IntegerField()),
                ('submitter', models.CharField(max_length=1024)),
                ('date', models.DateField(null=True, blank=True)),
                ('document', models.CharField(max_length=1024, blank=True)),
                ('opinion', models.CharField(max_length=1024, blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='suggestion',
            unique_together=set([('source_id', 'source_index')]),
        ),
    ]
