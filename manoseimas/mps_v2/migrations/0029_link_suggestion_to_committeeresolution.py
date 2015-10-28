# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0028_backfill_committeeresolutions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='source_id',
            field=models.ForeignKey(db_column=b'source_id', to_field=b'source_id', to='mps_v2.CommitteeResolution'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='suggestion',
            old_name='source_id',
            new_name='source_resolution',
        ),
        migrations.AlterUniqueTogether(
            name='suggestion',
            unique_together=set([('source_resolution', 'source_index')]),
        ),
        # Workaround for https://code.djangoproject.com/ticket/25621
        # D58bb2cf0b1407c8c24fa06b0cc34f38 is what you get from Django's
        # BaseDatabaseSchemaEditor._create_index_name() when you pass it
        # (model, ["source_id"], suffix="_fk_mps_v2_committeeresolution_source_id")
        migrations.RunSQL([], [
            "ALTER TABLE mps_v2_suggestion DROP FOREIGN KEY D58bb2cf0b1407c8c24fa06b0cc34f38",
        ]),
    ]
