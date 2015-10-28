# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify


def populate_slugs(apps, schema_editor):
    # borrowed from http://stackoverflow.com/questions/13243625/generate-slug-field-data-for-existing-entries-in-database
    Suggester = apps.get_model("mps_v2", "Suggester")

    for obj in Suggester.objects.filter(slug=""):
        slug = slugify(obj.title)[:110] # slug is max 120 chars long.
        obj.slug = slug
        suffix = 2
        # In case we have slugs alredy
        while Suggester.objects.filter(slug=obj.slug).exists():
            obj.slug = "%s-%d" % (slug, suffix)
            suffix = suffix + 1
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mps_v2', '0030_suggester_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]
