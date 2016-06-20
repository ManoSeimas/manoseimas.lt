# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy', '__first__'),
        ('compatibility_test', '0003_auto_20160601_0929'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicVoting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('factor', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='voting',
            name='topic',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='mp_positions',
            new_name='positions',
        ),
        migrations.DeleteModel(
            name='Voting',
        ),
        migrations.AddField(
            model_name='topicvoting',
            name='topic',
            field=models.ForeignKey(to='compatibility_test.Topic'),
        ),
        migrations.AddField(
            model_name='topicvoting',
            name='voting',
            field=models.ForeignKey(to='scrapy.Voting'),
        ),
        migrations.AddField(
            model_name='topic',
            name='votings',
            field=models.ManyToManyField(to='scrapy.Voting', through='compatibility_test.TopicVoting'),
        ),
    ]
