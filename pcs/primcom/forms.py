from django import forms

from .models import Trait, Taxonomy



class QueryDataForm(forms.Form):
    SPECIES_RAW = 'species_raw'
    SPECIES_CH = 'species_ch'
    SPECIES_WR = 'species_wr'
    TAXONOMY_OPTIONS = [
        (SPECIES_RAW, 'Raw data'),
        (SPECIES_CH, 'Corbett & Hill'),
        (SPECIES_WR, 'Wilson & Reeder'),
    ]

    traits = forms.MultipleChoiceField(choices=Trait.get_choices(False))
    taxonomy = forms.ChoiceField(
      choices=TAXONOMY_OPTIONS,
      widget=forms.RadioSelect(attrs={'class': 'Radio'}),
      initial='species_wr')
    species_raw = forms.MultipleChoiceField(
      choices=Taxonomy.get_choices_raw(False), required=False)
    species_ch = forms.MultipleChoiceField(
      choices=Taxonomy.get_choices_ch(False), required=False)
    species_wr = forms.MultipleChoiceField(
      choices=Taxonomy.get_choices_wr(False), required=False)
