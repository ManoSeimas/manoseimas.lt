# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('supporting', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompatTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PoliticalTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('mp_positions', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('source', models.URLField()),
                ('factor', models.PositiveIntegerField(default=1)),
                ('topic', models.ForeignKey(to='compatibility_test.PoliticalTopic')),
            ],
        ),
        migrations.AddField(
            model_name='politicaltopic',
            name='group',
            field=models.ForeignKey(to='compatibility_test.TestGroup'),
        ),
        migrations.AddField(
            model_name='politicaltopic',
            name='test',
            field=models.ForeignKey(to='compatibility_test.CompatTest'),
        ),
        migrations.AddField(
            model_name='argument',
            name='topic',
            field=models.ForeignKey(to='compatibility_test.PoliticalTopic'),
        ),
    ]
