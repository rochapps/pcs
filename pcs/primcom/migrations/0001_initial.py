# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('who_entered', models.CharField(max_length=3)),
                ('who_checked', models.CharField(max_length=3, blank=True, null=True)),
                ('site_name', models.CharField(max_length=100)),
                ('park_reserve_name', models.CharField(max_length=100, blank=True, null=True)),
                ('nation', models.CharField(max_length=100, blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicTraitData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('who_entered', models.CharField(max_length=3)),
                ('same_check', models.CharField(max_length=3, blank=True, null=True)),
                ('study_duration', models.FloatField()),
                ('is_wild', models.BooleanField(default=False)),
                ('trait_type', models.CharField(max_length=10, choices=[('min', 'Minimum'), ('max', 'Maximum'), ('mean', 'Mean'), ('median', 'Median'), ('stddev', 'S.D.')])),
                ('trait_value', models.FloatField()),
                ('sex', models.CharField(max_length=1, blank=True, null=True, choices=[('m', 'Male'), ('f', 'Female')])),
                ('sample_size', models.SmallIntegerField()),
                ('sample_type', models.CharField(max_length=20, null=True, choices=[('groups', 'Groups'), ('individuals', 'Individuals'), ('events', 'Events'), ('na', 'NA')])),
                ('basis', models.CharField(max_length=20, null=True, choices=[('present', 'Present'), ('converted', 'Converted'), ('calculated', 'Calculated'), ('inferred', 'Inferred')])),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(to='primcom.Location')),
            ],
        ),
        migrations.CreateModel(
            name='PublicVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('version_major', models.SmallIntegerField()),
                ('version_minor', models.SmallIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('file_tag', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('citation', models.CharField(max_length=100, null=True)),
                ('full_reference', models.CharField(max_length=1024)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('who_entered', models.CharField(max_length=3)),
                ('who_checked', models.CharField(max_length=3, blank=True, null=True)),
                ('species_reported_name', models.CharField(max_length=100)),
                ('binomial_wr05', models.CharField(max_length=100, blank=True, null=True)),
                ('binomial_corbhill', models.CharField(max_length=100, blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('category', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='TraitData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('who_entered', models.CharField(max_length=3)),
                ('same_check', models.CharField(max_length=3, blank=True, null=True)),
                ('study_duration', models.FloatField()),
                ('is_wild', models.BooleanField(default=False)),
                ('trait_type', models.CharField(max_length=10, choices=[('min', 'Minimum'), ('max', 'Maximum'), ('mean', 'Mean'), ('median', 'Median'), ('stddev', 'S.D.')])),
                ('trait_value', models.FloatField()),
                ('sex', models.CharField(max_length=1, blank=True, null=True, choices=[('m', 'Male'), ('f', 'Female')])),
                ('sample_size', models.SmallIntegerField()),
                ('sample_type', models.CharField(max_length=20, null=True, choices=[('groups', 'Groups'), ('individuals', 'Individuals'), ('events', 'Events'), ('na', 'NA')])),
                ('basis', models.CharField(max_length=20, null=True, choices=[('present', 'Present'), ('converted', 'Converted'), ('calculated', 'Calculated'), ('inferred', 'Inferred')])),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(to='primcom.Location')),
                ('reference', models.ForeignKey(to='primcom.Reference')),
                ('taxonomy', models.ForeignKey(to='primcom.Taxonomy')),
                ('trait', models.ForeignKey(to='primcom.Trait')),
            ],
        ),
        migrations.AddField(
            model_name='publictraitdata',
            name='reference',
            field=models.ForeignKey(to='primcom.Reference'),
        ),
        migrations.AddField(
            model_name='publictraitdata',
            name='taxonomy',
            field=models.ForeignKey(to='primcom.Taxonomy'),
        ),
        migrations.AddField(
            model_name='publictraitdata',
            name='trait',
            field=models.ForeignKey(to='primcom.Trait'),
        ),
        migrations.AddField(
            model_name='publictraitdata',
            name='version',
            field=models.ForeignKey(to='primcom.PublicVersion', null=True),
        ),
    ]
