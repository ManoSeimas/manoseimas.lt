# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0027_add_committeeresolution'),
    ]

    operations = [
        migrations.RunSQL([
            "INSERT IGNORE INTO mps_v2_committeeresolution (source_id, title) SELECT DISTINCT source_id, '' FROM mps_v2_suggestion",
            "UPDATE mps_v2_committeeresolution SET created_at = utc_timestamp() WHERE created_at is NULL",
            "UPDATE mps_v2_committeeresolution SET modified_at = utc_timestamp() WHERE modified_at is NULL",
        ], [
            "DELETE FROM mps_v2_committeeresolution",
        ]),
    ]
