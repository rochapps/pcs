# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0002_auto_20160621_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='traitdata',
            name='released',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='traitdata',
            name='version',
            field=models.FloatField(null=True, default=0),
        ),
    ]
