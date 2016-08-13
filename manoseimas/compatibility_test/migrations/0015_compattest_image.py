# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compatibility_test', '0014_topic_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='compattest',
            name='image',
            field=models.ImageField(null=True, upload_to='test_images', blank=True),
        ),
    ]
