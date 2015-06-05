# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0007_auto_20150605_0930'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupRanking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('votes_rank', models.IntegerField(default=0)),
                ('statement_count_rank', models.IntegerField(default=0)),
                ('long_statement_count_rank', models.IntegerField(default=0)),
                ('discusion_contribution_percentage_rank', models.IntegerField(default=0)),
                ('target', models.OneToOneField(related_name='ranking', to='mps_v2.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MPRanking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('votes_rank', models.IntegerField(default=0)),
                ('statement_count_rank', models.IntegerField(default=0)),
                ('long_statement_count_rank', models.IntegerField(default=0)),
                ('discusion_contribution_percentage_rank', models.IntegerField(default=0)),
                ('target', models.OneToOneField(related_name='ranking', to='mps_v2.ParliamentMember')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
