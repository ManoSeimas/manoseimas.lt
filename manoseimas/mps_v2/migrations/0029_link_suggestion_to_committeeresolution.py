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
    ]
