# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TraitData'
        db.create_table(u'primcom_traitdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('who_entered', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('who_checked', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('taxonomy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['primcom.Taxonomy'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['primcom.Location'])),
            ('reference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['primcom.Reference'])),
            ('trait', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['primcom.Trait'])),
            ('study_duration', self.gf('django.db.models.fields.FloatField')()),
            ('is_wild', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trait_value', self.gf('django.db.models.fields.FloatField')()),
            ('sample_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('trait_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'primcom', ['TraitData'])

        # Adding model 'Reference'
        db.create_table(u'primcom_reference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_reference', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'primcom', ['Reference'])

        # Adding model 'Location'
        db.create_table(u'primcom_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('who_entered', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('who_checked', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('park_reserve_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('nation', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'primcom', ['Location'])

        # Adding model 'Taxonomy'
        db.create_table(u'primcom_taxonomy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('who_entered', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('who_checked', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('species_reported_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('binomial_wr05', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('binomial_corbhill', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'primcom', ['Taxonomy'])

        # Adding model 'Trait'
        db.create_table(u'primcom_trait', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'primcom', ['Trait'])


    def backwards(self, orm):
        # Deleting model 'TraitData'
        db.delete_table(u'primcom_traitdata')

        # Deleting model 'Reference'
        db.delete_table(u'primcom_reference')

        # Deleting model 'Location'
        db.delete_table(u'primcom_location')

        # Deleting model 'Taxonomy'
        db.delete_table(u'primcom_taxonomy')

        # Deleting model 'Trait'
        db.delete_table(u'primcom_trait')


    models = {
        u'primcom.location': {
            'Meta': {'object_name': 'Location'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'park_reserve_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'who_checked': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'who_entered': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'primcom.reference': {
            'Meta': {'object_name': 'Reference'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'full_reference': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'primcom.taxonomy': {
            'Meta': {'object_name': 'Taxonomy'},
            'binomial_corbhill': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'binomial_wr05': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'species_reported_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'who_checked': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'who_entered': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'primcom.trait': {
            'Meta': {'object_name': 'Trait'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'primcom.traitdata': {
            'Meta': {'object_name': 'TraitData'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_wild': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Location']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Reference']"}),
            'sample_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'study_duration': ('django.db.models.fields.FloatField', [], {}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Taxonomy']"}),
            'trait': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Trait']"}),
            'trait_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'trait_value': ('django.db.models.fields.FloatField', [], {}),
            'who_checked': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'who_entered': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['primcom']