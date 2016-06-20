# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('mp_positions', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='politicaltopic',
            name='group',
        ),
        migrations.RemoveField(
            model_name='politicaltopic',
            name='test',
        ),
        migrations.AddField(
            model_name='testgroup',
            name='test',
            field=models.ForeignKey(to='compatibility_test.CompatTest', null=True),
        ),
        migrations.AlterField(
            model_name='argument',
            name='topic',
            field=models.ForeignKey(to='compatibility_test.Topic'),
        ),
        migrations.AlterField(
            model_name='voting',
            name='topic',
            field=models.ForeignKey(to='compatibility_test.Topic', null=True),
        ),
        migrations.DeleteModel(
            name='PoliticalTopic',
        ),
        migrations.AddField(
            model_name='testgroup',
            name='topics',
            field=models.ManyToManyField(to='compatibility_test.Topic'),
        ),
    ]
