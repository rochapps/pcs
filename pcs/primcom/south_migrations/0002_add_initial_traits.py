# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    TRAITS = (
        ('litter_size', 'Litter Size'),
        ('interbirth_interval', 'Interbirth Interval (yrs)'),
        ('gestation_length', 'Gestation Length (months)'),
        ('weaning_age', 'Weaning Age (days)'),
        ('age_sexual_maturity', 'Age Sexual Maturity (yrs)'),
        ('age_first_reproduction', 'Age 1st Reproduction (yrs)'),
        ('longevity', 'Longevity (yrs)'),
        ('female_body_weight', 'Female Body Weight (kg)'),
        ('mail_body_weight', 'Male Body Weight (kg)'),
        ('testes_mass', 'Testes Mass (g)'),
        ('brain_size', 'Brain Size (g)'),
        ('total_group_size', 'Group Size (Total)'),
        ('foraging_group_size', 'Group Size (Foraging)'),
        ('num_males', 'Number of Males'),
        ('num_females', 'Number of Females'),
        ('num_immature_individuals', 'Number of Immature Individuals'),
        ('num_dependent_individuals', 'Number of Dependent Infants'),
        ('pct_time_terrestrial', 'Percent Time Terrestrial'),
        ('home_range_area', 'Home Range Area (sq.km)'),
        ('defended_range', 'Defended Range (1/0)'),
        ('intergroup_conflict_females', 'Intergroup Conflict by Females (1/0)'),
        ('intergroup_conflict_males', 'Intergroup Conflict by Males (1/0)'),
        ('infanticide_females', 'Infanticide by Females (1/0)'),
        ('infanticide_males', 'Infanticide by Males (1/0)'),
        ('pct_range_overlap', 'Percent Range Overlap'),
        ('day_range', 'Day Range (km)'),
        ('pct_time_grooming', 'Percent Time Grooming'),
        ('diet_breadth', 'Diet Breadth (#)'),
        ('diet_pct_leaves', 'Diet: Percent Leaves'),
        ('diet_pct_fruit', 'Diet: Percent Fruit'),
        ('diet_pct_animal_prey', 'Diet: Percent Animal Prey'),
        ('diet_pct_gums', 'Diet: Percent Gums'),
        ('diet_pct_seeds', 'Diet: Percent Seeds'),
        ('diet_pct_flowers', 'Diet: Percent Flowers'),
        ('regular_dispersal_females', 'Regular Dispersal by Females (1/0)'),
        ('regular_dispersal_males', 'Regular Dispersal by Males (1/0)'),
        ('population_density', 'Population Density (#/sq.km)'),
        ('within_group_dispersion', 'Within Group Dispersion - Diameter (m)'),
        ('predated_bird', 'Predated by Birds (1/0)'),
        ('predated_mammal', 'Predated by Mammals (1/0)'),
        ('predated_reptile', 'Predated by Reptile (1/0)'),
        ('predated_human', 'Predated by Human (1/0)'),
        ('predated_domestic_animal', 'Predated by Domestic Animals (1/0)'),
        ('polyspecific_associations', 'Polyspecific Associations (1/0)'),
        ('all_male_groups', 'All Male Groups (1/0)'),
        ('paternal_care', 'Paternal Care (1/0)'),
        ('non_mother_female_care', 'Non-Mother Female Care (1/0)'),
    )
    
    def forwards(self, orm):
        for t in self.TRAITS:
            trait = orm.Trait()
            trait.code = t[0]
            trait.name = t[1]
            trait.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration. Deletion would result in data loss of changes.")
        
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
    symmetrical = True
