# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0003_auto_20160806_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traitdata',
            name='released',
            field=models.NullBooleanField(default=False),
        ),
    ]
