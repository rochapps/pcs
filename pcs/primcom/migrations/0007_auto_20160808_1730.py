# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0006_trait_website_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traitdata',
            name='released',
        ),
        migrations.AddField(
            model_name='traitdata',
            name='private',
            field=models.NullBooleanField(default=True),
        ),
    ]
