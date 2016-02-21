import codecs
import csv
import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView

from .models import TraitData, PublicTraitData, Trait, Taxonomy, Location, Reference, PublicVersion
from .forms import TraitDataForm, QueryDataForm


def _get_auto_fields(form):
    auto_fields = []
    for trait in Trait.objects.order_by('category', 'name'):
        trait_fields = []
        trait_fields.append(trait.name)
        for trait_type in TraitData.TRAIT_TYPES:
            trait_fields.append(form['auto_{0}_{1}'.format(
              trait.code,trait_type[0])])
        trait_fields.append(form['auto_{0}_sample_size'.format(trait.code)])
        trait_fields.append(form['auto_{0}_sample_type'.format(trait.code)])
        trait_fields.append(form['auto_{0}_basis'.format(trait.code)])
        trait_fields.append(form['auto_{0}_sex'.format(trait.code)])
        trait_fields.append(form['auto_{0}_notes'.format(trait.code)])
        auto_fields.append(trait_fields)
    return auto_fields

def _lookup_reference(reference_id):
    return Reference.objects.get(id=reference_id)

def _lookup_taxonomy(taxonomy_id):
    return Taxonomy.objects.get(id=taxonomy_id)

def _lookup_location(location_id):
    return Location.objects.get(id=location_id)

def home(request):
    ''' Handle requests for the "home" page.'''
    return render(request, 'primcom/index.html', {'home_active': True})

def info(request):
    ''' Handle requests for the "info" page.'''
    return render(request, 'primcom/info.html', {'info_active': True})


class Collaborators(TemplateView):
    template_name = 'primcom/collaborators.html'


def csv_data(request):
    '''Handle requests for CSV-export from the "query" page.'''

    if request.method == 'POST':
        form = QueryDataForm(request.POST)
        if form.is_valid():
            print("Form IS valid!")
            print(form.errors)
        else:
            print("Form is NOT valid!")
            print(form.errors)

        # Handle form processing
        #form = QueryDataForm(request.POST)

        # The 'taxonomy' field determines Trait names
        taxonomy_choice = request.POST.get('taxonomy',None)
        if taxonomy_choice == 'species_raw':
            taxonomy = 'raw'
        elif taxonomy_choice == 'species_wr':
            taxonomy = 'wr'
        elif taxonomy_choice == 'species_ch':
            taxonomy = 'ch'
        import pprint
        species = request.POST.getlist(taxonomy_choice)
        print("Species:")
        pprint.pprint(species)
        traits = request.POST.getlist('traits')
        print("Traits:")
        pprint.pprint(traits)

        for q in request.POST:
            print("{0} == {1}".format(q,request.POST.getlist(q)))

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response_filename = 'pcs_results-v{0}-{1}.csv'.format(
      PublicVersion.get_latest_version(),
      datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    response['Content-Disposition'] = 'attachment; ' \
      'filename={0}'.format(response_filename)
    writer = csv.writer(response, delimiter='\t')
    # Add the Excel BOM for UTF-8 encoding
    response.write(codecs.BOM_UTF8)
    objects_to_display = PublicTraitData.objects.all().filter(trait__pk__in=traits).filter(taxonomy__pk__in=species)
    writer.writerow(PublicTraitData.get_csv_headers())
    for g in objects_to_display:
        writer.writerow(g.get_csv_data(species_taxonomy=taxonomy))
    return response

def query(request):
    '''Handle requests for the "query" page.'''

    context = dict()
    if request.method == 'POST':
        form = QueryDataForm(request.POST)
        if form.is_valid():
            print("Form IS valid!")
            print(form.errors)
        else:
            print("Form is NOT valid!")
            context['form'] = QueryDataForm(request.POST)
    else:
        context['form'] = QueryDataForm()
    context['query_active'] = True
    context['traits_by_category'] = Trait.get_all_by_category()
    return render_to_response(
      'primcom/query.html', context, context_instance=RequestContext(request))

def methods(request):
    ''' Handle requests for the "methods" page.'''
    return render(request, 'primcom/methods.html', {'methods_active': True})

def archive(request):
    ''' Handle requests for the "archive" page.'''

    context = dict()
    context['archives'] = [
      {'date', 'size', 'link', 'notes'}
    ]
    context['archive_active'] = True
    return render_to_response(
      'primcom/archive.html', context, context_instance=RequestContext(request))

def contact(request):
    ''' Handle requests for the "contact" page.'''
    return render(request, 'primcom/contact.html', {'contact_active': True})

def add(request):
    '''Handle requests for the "add" page for a TraitData object.'''

    context = dict()
    if request.method == 'POST':
        form = TraitDataForm(request.POST)
        if form.is_valid():
            # Handle Taxonomy data
            if int(form.cleaned_data['taxonomy_id']) == -1:
                taxonomy = Taxonomy()
                taxonomy.who_entered = form.cleaned_data['who_entered']
                taxonomy.species_reported_name = \
                  form.cleaned_data['species_reported_name']
                taxonomy.save()
                messages.success(request, 'New taxonomy successfully saved.')
            else:
                taxonomy = _lookup_taxonomy(
                  form.cleaned_data['taxonomy_id'])

            # Handle Location data
            if int(form.cleaned_data['location_id']) == -1:
                location = Location()
                location.who_entered = form.cleaned_data['who_entered']
                location.site_name = form.cleaned_data['site_name']
                location.park_reserve_name = \
                  form.cleaned_data['park_reserve_name']
                location.nation = form.cleaned_data['nation']
                location.latitude = form.cleaned_data['latitude']
                location.longitude = form.cleaned_data['longitude']
                location.notes = form.cleaned_data['location_notes']
                location.save()
                messages.success(request, 'New location successfully saved.')
            else:
                location = _lookup_location(form.cleaned_data['location_id'])

            # Handle Reference data
            if int(form.cleaned_data['reference_id']) == -1:
                reference = Reference()
                reference.citation = form.cleaned_data['citation']
                reference.full_reference = form.cleaned_data['full_reference']
                reference.abstract = form.cleaned_data['abstract']
                reference.notes = form.cleaned_data['notes']
                reference.save()
                messages.success(request, 'New reference successfully saved.')
            else:
                reference = _lookup_reference(form.cleaned_data['reference_id'])

            # Handle TraitData data
            td_count = 0
            for td in Trait.objects.all():
                for tt in TraitData.TRAIT_TYPES:
                    tt_code = tt[0]
                    trait_data = form.cleaned_data.get('auto_{0}_{1}'.format(
                      td.code, tt_code), None)
                    if trait_data not in (None, ''):
                        traitdata = TraitData()
                        traitdata.who_entered = form.cleaned_data.get(
                          'who_entered')
                        traitdata.taxonomy = taxonomy
                        traitdata.location = location
                        traitdata.reference = reference
                        traitdata.trait = td
                        traitdata.trait_type = tt_code
                        traitdata.trait_value = trait_data
                        traitdata.sample_size = form.cleaned_data.get(
                          'auto_{0}_sample_size'.format(td.code))
                        traitdata.sample_type = form.cleaned_data.get(
                          'auto_{0}_sample_type'.format(td.code))
                        traitdata.basis = form.cleaned_data.get(
                          'auto_{0}_basis'.format(td.code))
                        traitdata.study_duration = form.cleaned_data.get(
                          'study_duration')
                        traitdata.sex = form.cleaned_data.get(
                          'auto_{0}_sex'.format(td.code))
                        traitdata.is_wild = form.cleaned_data.get('is_wild')
                        traitdata.notes = form.cleaned_data.get(
                          'auto_{0}_notes'.format(td.code, tt_code))
                        traitdata.save()
                        td_count += 1

            if td_count:
                messages.success(request,
                  'New trait data ({0}) successfully added.'.format(td_count))
            return redirect('primcom.views.add')
        else:
            context['form'] = TraitDataForm(request.POST)
    else:
        context['form'] = TraitDataForm()

    # The initial "add" page
    context['auto_fields'] = _get_auto_fields(context['form'])
    context['add_active'] = True
    return render_to_response('primcom/traitdata_form.html', context, context_instance=RequestContext(request))
