# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import sboard.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node', sboard.models.NodeForeignKey(max_length=16, db_index=True)),
                ('profile', sboard.models.NodeForeignKey(max_length=16)),
                ('profile_type', models.IntegerField(default=0, choices=[(0, 'User'), (1, 'Member of Parliament'), (2, 'Fraction'), (3, 'Group')])),
                ('position', models.DecimalField(max_digits=7, decimal_places=4, db_index=True)),
                ('participation', models.DecimalField(default=Decimal('1'), max_digits=7, decimal_places=4, db_index=True)),
            ],
        ),
    ]
