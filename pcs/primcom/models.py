from datetime import datetime

from django.db import models


class PublicVersion(models.Model):
    version_major = models.SmallIntegerField()
    version_minor = models.SmallIntegerField()
    description = models.TextField(blank=True,null=True)
    file_tag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return "{0}.{1}".format(self.version_major, self.version_minor)

    @classmethod
    def get_latest_version(cls):
        return PublicVersion.objects.get(pk=cls.objects.all().order_by('-created_at').values()[0]['id'])


class TraitData(models.Model):
    who_entered = models.CharField(max_length=3)
    same_check = models.CharField(max_length=3, blank=True, null=True)
    taxonomy = models.ForeignKey('Taxonomy')
    location = models.ForeignKey('Location')
    reference = models.ForeignKey('Reference')
    trait = models.ForeignKey('Trait')
    study_duration = models.FloatField()
    is_wild = models.BooleanField(default=False)
    TRAIT_TYPES = (
        ('min', 'Minimum'),
        ('max', 'Maximum'),
        ('mean', 'Mean'),
		('median', 'Median'),
		('stddev', 'S.D.'),
    )
    trait_type = models.CharField(max_length=10, choices=TRAIT_TYPES)
    trait_value = models.FloatField()
    SEX_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'))
    sex = models.CharField(max_length=1, blank=True, null=True,
      choices=SEX_CHOICES)
    sample_size = models.SmallIntegerField()
    SAMPLE_TYPES = (
        ('groups', 'Groups'),
        ('individuals', 'Individuals'),
        ('events', 'Events'),
        ('na', 'NA'),
    )
    sample_type = models.CharField(max_length=20, null=True,
      choices=SAMPLE_TYPES)
    BASIS_CHOICES = (
        ('present', 'Present'),
        ('converted', 'Converted'),
        ('calculated', 'Calculated'),
        ('inferred', 'Inferred'),
    )
    basis = models.CharField(max_length=20, null=True,
      choices=BASIS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PublicTraitData(models.Model):
    who_entered = models.CharField(max_length=3)
    same_check = models.CharField(max_length=3, blank=True, null=True)
    taxonomy = models.ForeignKey('Taxonomy')
    location = models.ForeignKey('Location')
    reference = models.ForeignKey('Reference')
    trait = models.ForeignKey('Trait')
    study_duration = models.FloatField()
    is_wild = models.BooleanField(default=False)
    TRAIT_TYPES = (
        ('min', 'Minimum'),
        ('max', 'Maximum'),
        ('mean', 'Mean'),
		('median', 'Median'),
		('stddev', 'S.D.'),
    )
    trait_type = models.CharField(max_length=10, choices=TRAIT_TYPES)
    trait_value = models.FloatField()
    SEX_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'))
    sex = models.CharField(max_length=1, blank=True, null=True,
      choices=SEX_CHOICES)
    sample_size = models.SmallIntegerField()
    SAMPLE_TYPES = (
        ('groups', 'Groups'),
        ('individuals', 'Individuals'),
        ('events', 'Events'),
        ('na', 'NA'),
    )
    sample_type = models.CharField(max_length=20, null=True,
      choices=SAMPLE_TYPES)
    BASIS_CHOICES = (
        ('present', 'Present'),
        ('converted', 'Converted'),
        ('calculated', 'Calculated'),
        ('inferred', 'Inferred'),
    )
    basis = models.CharField(max_length=20, null=True,
      choices=BASIS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.ForeignKey('PublicVersion', null=True)

    @classmethod
    def get_csv_headers(cls):
        '''Return a sequence to be used as CSV header fields.'''

        csv_headers = (
            'species_name',
            'species_reported_name',
            'site_name',
            'park_reserve_name',
            'nation',
            'latitude',
            'longitude',
            'citation',
            'full_reference',
            'trait_name',
            'study_duration',
            'is_wild',
            'trait_type',
            'trait_value',
            'sample_size',
            'sample_type',
            'basis',
            'sex',
            'notes')
        return csv_headers

    def get_csv_data(self, species_taxonomy=None):
        '''Return a sequence to be used as CSV data.'''

        csv_values = (
            self.taxonomy.species_name(species_taxonomy),
            self.taxonomy.species_reported_name,
            self.location.site_name,
            self.location.park_reserve_name.encode('utf-8'),
            self.location.nation,
            self.location.latitude,
            self.location.longitude,
            self.reference.citation.encode('utf-8'),
            self.reference.full_reference.encode('utf-8'),
            self.trait.name,
            self.study_duration,
            self.is_wild,
            self.trait_type,
            self.trait_value,
            self.sample_size,
            self.sample_type,
            self.basis,
            self.sex,
            self.notes)
        return [v for v in csv_values]

    @classmethod
    def promote_devel(cls):
      """Promote the data in the "development" TraitData to the public site."""

      # Delete all existing models
      PublicTraitData.objects.all().delete()

      # Create new objects from the data of the "development" objects
      td_data = TraitData.objects.all().values()
      for td in td_data:
        ptd = PublicTraitData(**td)
        ptd.save()


class Reference(models.Model):
    citation = models.CharField(max_length=100, null=True)
    full_reference = models.CharField(max_length=1024)
    abstract = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_choices(cls):
        references = [
          (reference.id,
          reference.full_reference[:130] + '..' \
            if len(reference.full_reference) > 132 else \
            reference.full_reference)
          for reference in cls.objects.all().order_by('full_reference') ]
        references.insert(0, (-1, 'New...'))
        return references


#class PublicReference(Reference):
#    version = models.ForeignKey('PublicVersion')


class Location(models.Model):
    who_entered = models.CharField(max_length=3)
    who_checked = models.CharField(max_length=3, blank=True, null=True)
    site_name = models.CharField(max_length=100)
    park_reserve_name = models.CharField(max_length=100, blank=True, null=True)
    nation = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @classmethod
    def get_choices(cls):
        sites = [
          (location.id,
          location.site_name[:130] + '..' \
            if len(location.site_name) > 132 else \
            location.site_name)
          for location in cls.objects.all().order_by('site_name') ]
        sites.insert(0, (-1, 'New...'))
        return sites


#class PublicLocation(Location):
#    version = models.ForeignKey('PublicVersion')


class Taxonomy(models.Model):
    who_entered = models.CharField(max_length=3)
    who_checked = models.CharField(max_length=3, blank=True, null=True)
    species_reported_name = models.CharField(max_length=100)
    binomial_wr05 = models.CharField(max_length=100, blank=True, null=True)
    binomial_corbhill = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def species_name(self, species_taxonomy=None):
        if species_taxonomy == 'raw' or species_taxonomy == None:
            name_string = self.species_reported_name
        if species_taxonomy == 'wr':
            if self.binomial_wr05:
                name_string = self.binomial_wr05
            else:
                name_string = "({0})".format(self.species_reported_name)
        if species_taxonomy == 'ch':
            if self.binomial_corbhill:
                name_string = self.binomial_corbhill
            else:
                name_string = "({0})".format(self.species_reported_name)
        return name_string


#    @classmethod
#    def get_choices(cls, tax_def=None, include_new=True):
#        names = []
#        import pprint
#        for taxonomy in cls.objects.all().order_by(field_name,'species_reported_name'):
#            tax_name = str()
#            if tax_def:
#                if tax_def == 'wr':
#                    tax_name = taxonomy.binomial_wr05
#                elif tax_def == 'ch':
#                    tax_name = taxonomy.binomial_corbhill
#                if tax_name == '' and taxonomy.species_reported_name:
#                    print 'No name for {0}; using species_reported_name'.format(taxonomy.id)
#                    tax_name = '[{0}]'.format(taxonomy.species_reported_name)
#                else:
#                    print 'No species_reported_name for {0}; using id'.format(taxonomy.id)
#                    tax_name = '({0})'.format(taxonomy.id)
#            if len(tax_name) > 132:
#                tax_name = '{0}..'.format(tax_name[:130])
#            names.append(tax_name)
#        pprint.pprint(names)
#        return names

    @classmethod
    def get_choices_raw(cls, include_new=True):
        names = []
        for taxonomy in cls.objects.all().order_by('species_reported_name'):
            tax_name = taxonomy.species_reported_name
            if len(tax_name) > 132:
                tax_name = '{0}..'.format(tax_name[:130])
            names.append((taxonomy.id, tax_name))
        return names

    @classmethod
    def get_choices_ch(cls, include_new=True):
        names = []
        for taxonomy in cls.objects.all().order_by('species_reported_name'):
            tax_name = taxonomy.binomial_corbhill
            if tax_name is None:
                tax_name = '({0})'.format(taxonomy.species_reported_name)
            if len(tax_name) > 132:
                tax_name = '{0}..'.format(tax_name[:130])
            names.append((taxonomy.id, tax_name))
        return names

    @classmethod
    def get_choices_wr(cls, include_new=True):
        names = []
        for taxonomy in cls.objects.all().order_by('species_reported_name'):
            tax_name = taxonomy.binomial_wr05
            if tax_name is None:
                tax_name = '({0})'.format(taxonomy.species_reported_name)
            if len(tax_name) > 132:
                tax_name = '{0}..'.format(tax_name[:130])
            names.append((taxonomy.id, tax_name))
        return names


#class PublicTaxonomy(Taxonomy):
#    version = models.ForeignKey('PublicVersion')


class Trait(models.Model):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    category = models.SmallIntegerField(default=1)

    CATEGORY_MAP = {
      1: 'Life History',
      2: 'Dispersal',
      3: 'Morphology',
      4: 'Demography',
      5: 'Diet',
      6: 'Ranging & Activity',
      7: 'Agonism',
      8: 'Predation'
    }

    @classmethod
    def get_choices(cls, include_new=True):
        traits = [ (trait.id, trait.code) for trait in cls.objects.all().order_by('category') ]
        if include_new:
            traits.insert(0, (-1, 'New...'))
        return traits

    @classmethod
    def get_all_by_category(cls):
        '''Return a structure organizing traits by category.'''

        structure = dict()
        for k in cls.CATEGORY_MAP.keys():
            structure[k] = dict()
            structure[k]['name'] = cls.CATEGORY_MAP[k]
            structure[k]['traits'] = list()

        for t in cls.objects.all().order_by('category','name'):
            structure[t.category]['traits'].append((t.id,t.name))

        import pprint
        pprint.pprint(structure)

        trait_categories = list()
        for k in structure.keys():
            trait_categories.append((k,structure[k]['name'],structure[k]['traits']))
        return trait_categories


#class PublicTrait(Trait):
#    version = models.ForeignKey('PublicVersion')
