# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def make_everything_public(apps, schema_editor):
    # makes everything not private
    TraitData = apps.get_model('primcom', 'TraitData')
    for data in TraitData.objects.all():
        data.private = False
        data.save()


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0007_auto_20160808_1730'),
    ]

    operations = [
        migrations.RunPython(make_everything_public),
    ]
