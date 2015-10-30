# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0029_link_suggestion_to_committeeresolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggester',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(populate_from=b'title', max_length=120, editable=False, blank=True),
        ),
    ]

