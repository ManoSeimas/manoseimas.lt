# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0027_add_committeeresolution'),
    ]

    operations = [
        migrations.RunSQL("""
           INSERT IGNORE INTO mps_v2_committeeresolution (source_id, title, source)
           SELECT DISTINCT source_id, '', source FROM mps_v2_suggestion
        """),
    ]
