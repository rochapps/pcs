# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Location.created_at'
        db.alter_column(u'primcom_location', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))

    def backwards(self, orm):

        # Changing field 'Location.created_at'
        db.alter_column(u'primcom_location', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(1900, 1, 1, 0, 0)))

    models = {
        u'primcom.location': {
            'Meta': {'object_name': 'Location'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
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
            'citation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
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
            'category': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'primcom.traitdata': {
            'Meta': {'object_name': 'TraitData'},
            'basis': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_wild': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Location']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Reference']"}),
            'same_check': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'sample_size': ('django.db.models.fields.SmallIntegerField', [], {}),
            'sample_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'study_duration': ('django.db.models.fields.FloatField', [], {}),
            'taxonomy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Taxonomy']"}),
            'trait': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['primcom.Trait']"}),
            'trait_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'trait_value': ('django.db.models.fields.FloatField', [], {}),
            'who_entered': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['primcom']