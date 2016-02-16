from django import forms
from django.forms import TextInput, Textarea

from models import TraitData, Trait, Reference, Location, Taxonomy


class TraitDataForm(forms.Form):
    who_entered = forms.CharField(
      max_length=3, 
      widget=TextInput(attrs={'size': 3}))
    reference_id = forms.ChoiceField(
      choices=Reference.get_choices(), 
      label='Reference')
    citation = forms.CharField(
      max_length=100,
      required=False, 
      widget=TextInput(attrs={'size': 150}))
    full_reference = forms.CharField(
      max_length=1024, 
      required=False, 
      widget=TextInput(attrs={'size': 150}))
    taxonomy_id = forms.ChoiceField(
      choices=Taxonomy.get_choices_raw(),
      label='Taxonomy')
    species_reported_name = forms.CharField(
      max_length=100,
      required=False)
    location_id = forms.ChoiceField(
      choices=Location.get_choices(),
      label='Location')
    site_name = forms.CharField(
      max_length=100, 
      required=False)
    park_reserve_name = forms.CharField(
      max_length=100, 
      required=False)
    nation = forms.CharField(
      max_length=100, 
      required=False)
    latitude =  forms.FloatField(
      required=False, 
      widget=TextInput(attrs={'size': 4}))
    longitude = forms.FloatField(
      required=False, 
      widget=TextInput(attrs={'size': 4}))
    location_notes = forms.CharField(
      label='Notes', 
      required=False, 
      widget=Textarea(attrs={'rows': 6, 'cols': 100}))
    notes = forms.CharField(
      required=False,
      widget=Textarea(attrs={'rows': 6, 'cols': 100}))
    abstract = forms.CharField(
      required=False, 
      widget=Textarea(attrs={'rows': 6, 'cols': 100}))
    study_duration = forms.FloatField(
      label='Study Duration', 
      required=False,
      widget=TextInput(attrs={'size': 4}))
    is_wild = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(TraitDataForm, self).__init__(*args, **kwargs)

        self.fields['reference_id'].choices = \
          Reference.get_choices()
        self.fields['taxonomy_id'].choices = \
          Taxonomy.get_choices()
        self.fields['location_id'].choices = \
          Location.get_choices()

        for trait in Trait.objects.all():
            for type_code, type_label in TraitData.TRAIT_TYPES:
                self.fields['auto_%s_%s' % (trait.code, type_code)] = \
                  forms.FloatField(required=False,
                    label='{0} {1}'.format(trait.name, type_label),
                    widget=TextInput(attrs={'size':4}))
            self.fields['auto_{0}_sample_size' .format(trait.code)] = \
              forms.IntegerField(label='Sample Size', required=False,
                widget=TextInput(attrs={'size': 4}))
            self.fields['auto_{0}_sample_type' .format(trait.code)] = \
              forms.ChoiceField(label='Sample Type', required=False,
                choices=self._prepend_empty_choice(TraitData.SAMPLE_TYPES))
            self.fields['auto_{0}_basis' .format(trait.code)] = \
              forms.ChoiceField(label='Basis', required=False,
                choices=self._prepend_empty_choice(TraitData.BASIS_CHOICES))
            self.fields['auto_{0}_sex' .format(trait.code)] = \
              forms.ChoiceField(label='Sex', required=False,
                choices=self._prepend_empty_choice(TraitData.SEX_CHOICES))
            self.fields['auto_{0}_notes' .format(trait.code)] = \
              forms.CharField(label='Notes', required=False,
                widget=TextInput(attrs={'size': 30}))

    def _prepend_empty_choice(self, real_choices):
        choices = [('','')]
        for c in real_choices:
          choices.append(c)
        return choices

    def clean(self):
        cleaned_data = super(TraitDataForm, self).clean()

        # Citation, full reference must be specified when adding a new Reference
        if int(cleaned_data['reference_id']) == -1:
            if not cleaned_data.get('citation'):
                self._errors['citation'] = self.error_class([
                  'This field is required.'])
                del cleaned_data['citation']

            if not cleaned_data.get('full_reference'):
                self._errors['full_reference'] = self.error_class([
                  'This field is required.'])
                del cleaned_data['full_reference']
            
        # Species reported name must be specified when adding a new Taxonomy
        if int(cleaned_data['taxonomy_id']) == -1:
            if not cleaned_data.get('species_reported_name'):
                self._errors['species_reported_name'] = self.error_class([
                  'This field is required.'])
                del cleaned_data['species_reported_name']

        # Site name must be specified when adding a new Location
        if int(cleaned_data['location_id']) == -1:
            if not cleaned_data.get('site_name'):
                self._errors['site_name'] = self.error_class([
                  'This field is required.'])
                del cleaned_data['site_name']

        # Sample size/type and study duration required for trait data.
        for td in Trait.objects.all():
            for tt in TraitData.TRAIT_TYPES:
                tt_code = tt[0]
                if cleaned_data.get('auto_{0}_{1}'.format(
                  td.code, tt_code), None):
                    if not cleaned_data.get('auto_{0}_sample_size'.format(
                      td.code), None):
                        raise forms.ValidationError(
                          'Sample size is required for {0}.'.format(td.name))
                    if not cleaned_data.get('auto_{0}_sample_type'.format(
                      td.code), None):
                        raise forms.ValidationError(
                          'Sample type is required for {0}.'.format(td.name))
                    if not cleaned_data.get('auto_{0}_basis'.format(
                      td.code), None):
                        raise forms.ValidationError(
                          'Basis is required for {0}.'.format(td.name))
                    if not cleaned_data.get('study_duration'.format(
                      td.code), None):
                        raise forms.ValidationError(
                          'Study duration is required for {0}.'.format(td.name))

        # Always return the full collection of cleaned data.
        return cleaned_data


class QueryDataForm(forms.Form):
    traits = forms.MultipleChoiceField(
      choices=Trait.get_choices(False))
    #results = forms.MultipleChoiceField(
    #  choices=(
    #    (1, 'Raw data'),
    #    (2, 'Summary data'),
    #  ),
    #  initial=2)
    taxonomy = forms.ChoiceField(
      choices=(
        ('species_raw', 'Raw data'),
        ('species_ch', 'Corbett & Hill'),
        ('species_wr', 'Wilson & Reeder'),
      ),
      widget=forms.RadioSelect(attrs={'class': 'Radio'}),
      initial='species_wr')
    species_raw = forms.MultipleChoiceField(
      choices=Taxonomy.get_choices_raw(False), required=False)
    species_ch = forms.MultipleChoiceField(
      choices=Taxonomy.get_choices_ch(False), required=False)
    species_wr = forms.MultipleChoiceField(
      choices=Taxonomy.get_choices_wr(False), required=False)
