# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stenogram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('source_id', models.CharField(max_length=16, db_index=True)),
                ('date', models.DateField()),
                ('sitting_no', models.IntegerField()),
                ('sitting_name', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StenogramStatement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('speaker_name', models.CharField(max_length=64)),
                ('text', models.TextField()),
                ('speaker', models.ForeignKey(related_name='statements', blank=True, to='mps_v2.ParliamentMember', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StenogramTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('stenogram', models.ForeignKey(related_name='topics', to='mps_v2.Stenogram')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='stenogramstatement',
            name='topic',
            field=models.ForeignKey(related_name='statements', to='mps_v2.StenogramTopic'),
        ),
    ]
