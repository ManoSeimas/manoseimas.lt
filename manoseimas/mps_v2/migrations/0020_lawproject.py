# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0019_auto_20150615_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='LawProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('source_id', models.CharField(unique=True, max_length=16, db_index=True)),
                ('date', models.DateField()),
                ('project_name', models.TextField()),
                ('project_number', models.CharField(max_length=32)),
                ('project_url', models.URLField()),
                ('date_passed', models.DateField(null=True, blank=True)),
                ('passing_source_id', models.CharField(db_index=True, max_length=16, null=True, blank=True)),
                ('passing_doc_number', models.CharField(max_length=32, null=True, blank=True)),
                ('passing_doc_url', models.URLField(null=True, blank=True)),
                ('proposers', models.ManyToManyField(related_name='law_projects', to='mps_v2.ParliamentMember')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
