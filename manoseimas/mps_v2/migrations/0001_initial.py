# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import manoseimas.mps_v2.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('type', models.CharField(max_length=64, choices=[(b'group', 'Group'), (b'committee', 'Committee'), (b'commission', 'Commission'), (b'fraction', 'Fraction'), (b'parliament', 'Parliament')])),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(max_length=128)),
                ('since', models.DateField(null=True, blank=True)),
                ('until', models.DateField(null=True, blank=True)),
                ('group', models.ForeignKey(to='mps_v2.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParliamentMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=manoseimas.mps_v2.models.get_mp_full_name, editable=False)),
                ('source_id', models.CharField(max_length=16)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('date_of_birth', models.CharField(max_length=16, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('candidate_page', models.URLField(null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'/tmp/images', blank=True)),
                ('term_of_office', models.CharField(max_length=32, null=True, blank=True)),
                ('office_address', models.TextField(null=True, blank=True)),
                ('constituency', models.CharField(max_length=128, null=True, blank=True)),
                ('party_candidate', models.BooleanField(default=True)),
                ('biography', models.TextField(null=True, blank=True)),
                ('groups', models.ManyToManyField(to='mps_v2.Group', through='mps_v2.GroupMembership')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PoliticalParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='parliamentmember',
            name='raised_by',
            field=models.ForeignKey(blank=True, to='mps_v2.PoliticalParty', null=True),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='member',
            field=models.ForeignKey(to='mps_v2.ParliamentMember'),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('name', 'type')]),
        ),
    ]
