# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0004_auto_20160806_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='trait',
            name='output_label',
            field=models.CharField(null=True, max_length=256, blank=True),
        ),
    ]
