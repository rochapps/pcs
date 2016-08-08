# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0008_auto_20160808_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traitdata',
            name='version',
            field=models.FloatField(null=True, default=None, blank=True),
        ),
    ]
