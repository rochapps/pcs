# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primcom', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('site_name',)},
        ),
        migrations.AlterModelOptions(
            name='reference',
            options={'ordering': ('citation',)},
        ),
    ]
