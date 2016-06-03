# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('key', models.CharField(max_length=255)),
                ('value', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('key', models.CharField(max_length=255)),
                ('value', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('key', models.CharField(max_length=255)),
                ('value', jsonfield.fields.JSONField(default=dict)),
                ('name', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField()),
                ('source', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
