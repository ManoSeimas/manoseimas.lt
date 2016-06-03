# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0002_auto_20160531_1913'),
        ('mps_v2', '0031_suggester_slug_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='topic',
            field=models.ForeignKey(related_name='stenogram_votings', to='compatibility_test.Topic', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='voting',
            unique_together=set([('topic', 'stenogram_topic')]),
        ),
        migrations.RemoveField(
            model_name='voting',
            name='node',
        ),
    ]
