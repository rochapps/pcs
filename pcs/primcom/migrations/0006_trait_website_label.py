# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0005_trait_output_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='trait',
            name='website_label',
            field=models.CharField(max_length=256, blank=True, null=True),
        ),
    ]
