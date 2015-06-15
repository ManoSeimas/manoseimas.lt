# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def recreate_slugs(apps, schema_editor):
    for model in ['ParliamentMember', 'Group']:
        cls = apps.get_model('mps_v2', model)
        field = filter(lambda field: field.name == 'slug',
                       cls._meta.fields)[0]
        field.overwrite = True  # XXX HAX to force slug overwrite
        for item in cls.objects.all():
            item.slug = None
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0018_auto_20150615_1600'),
    ]

    operations = [
        migrations.RunPython(recreate_slugs)
    ]
