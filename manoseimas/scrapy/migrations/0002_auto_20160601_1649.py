# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('value', jsonfield.fields.JSONField(default=dict)),
                ('p_asm_id', models.CharField(max_length=16)),
                ('fraction', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=255)),
                ('vote', models.SmallIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='person',
            name='p_asm_id',
            field=models.CharField(default=b'', max_length=16),
        ),
        migrations.AlterField(
            model_name='person',
            name='key',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='key',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='voting',
            name='key',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='voting',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
