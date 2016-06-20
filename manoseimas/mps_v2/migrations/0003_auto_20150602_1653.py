# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0002_auto_20150602_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node', models.CharField(max_length=16)),
                ('timestamp', models.DateTimeField()),
                ('stenogram_topic', models.ForeignKey(related_name='votings', to='mps_v2.StenogramTopic')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set([('stenogram_topic', 'node')]),
        ),
    ]
