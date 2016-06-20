# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy', '0003_personvote_timestamp'),
        ('mps_v2', '0032_auto_20160531_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='voting',
            field=models.ForeignKey(related_name='stenogram_votings', to='scrapy.Voting', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set([('voting', 'stenogram_topic')]),
        ),
        migrations.RemoveField(
            model_name='voting',
            name='topic',
        ),
    ]
