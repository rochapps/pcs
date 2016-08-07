from functools import reduce
import os
import shutil
import time

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from .models import TraitData, Trait, Taxonomy, Location, Reference
from .forms import QueryDataForm, TraitDataForm
from .utils import write_raw_data_file, write_mean_data_file, write_location_data_file, write_location_references_file


def _get_auto_fields(form):
    auto_fields = []
    for trait in Trait.objects.order_by('category', 'name'):
        trait_fields = []
        trait_fields.append(trait.website_label)
        for trait_type in TraitData.TRAIT_TYPES:
            trait_fields.append(form['auto_{0}_{1}'.format(
                    trait.code, trait_type[0])])
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


from django.shortcuts import redirect

@require_POST
def csv_data(request):
    '''Handle requests for CSV-export from the "query" page.'''

    form = QueryDataForm(request.POST)
    if form.is_valid():
        print("Form IS valid!")
        print(form.errors)
    else:
        print("Form is NOT valid!")
        print(form.errors)
        messages.error(request, "Please fix the following errors: {0}".format(form.errors))
        return redirect(query)
    # The 'taxonomy' field determines Trait names
    taxonomy_choice = request.POST.get('taxonomy', None)
    if taxonomy_choice == 'species_raw':
        taxonomy = 'raw'
        taxonomy_field = 'species_reported_name'
    elif taxonomy_choice == 'species_wr':
        taxonomy = 'wr'
        taxonomy_field = 'binomial_wr05'
    elif taxonomy_choice == 'species_ch':
        taxonomy = 'ch'
        taxonomy_field = 'binomial_corbhill'
    else:
        taxonomy_field = 'species_reported_name'
        taxonomy = 'raw'
    unique_species = Taxonomy.objects.in_bulk(request.POST.getlist(taxonomy_choice))
    # get names for all unique species
    unique_species_name = [getattr(taxonomy, taxonomy_field) for _key, taxonomy in unique_species.items()]
    # get all including duplicates
    q_list = map(lambda n: Q(**{'{0}__in'.format(taxonomy_field): unique_species_name}), unique_species_name)
    q_list = reduce(lambda a, b: a | b, q_list)
    species = Taxonomy.objects.filter(q_list)
    traits = request.POST.getlist('traits')
    traits = Trait.objects.in_bulk(traits)
    qs = TraitData.objects.all(
        ).filter(
            trait__in=traits,
            taxonomy=species,
            released=True,
        ).order_by(
            'taxonomy__species_reported_name',
            'trait__name',
            'sex',
        ).select_related(
            'trait',
            'taxonomy',
        )
    locations = set([trait.location.id for trait in qs])
    locations = Location.objects.filter(id__in=locations)
    references = set([trait.reference.id for trait in qs])
    references = Reference.objects.filter(id__in=references)
    # make a directory for current download
    now = time.strftime("%b-%d-%Y-%H%M%S", time.gmtime(time.time()))
    tempdir = os.path.join(settings.MEDIA_ROOT, 'downloads', now)
    os.mkdir(tempdir)
    # create files to be downloaded
    write_mean_data_file(os.path.join(tempdir, 'mean_values.csv'), qs, traits, taxonomy)
    write_raw_data_file(os.path.join(tempdir, 'raw_data.csv'), qs, traits, taxonomy)
    write_location_data_file(os.path.join(tempdir, 'locations.csv'), locations)
    write_location_references_file(os.path.join(tempdir, 'references.csv'), references)
    # zip all files we created
    zip_file_name = shutil.make_archive(os.path.join(settings.MEDIA_ROOT, 'downloads', "10ktraits_{0}".format(now)), 'zip', tempdir)
    shutil.rmtree(tempdir)
    return redirect(zip_file_name.replace(settings.MEDIA_ROOT, settings.MEDIA_URL))


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
                taxonomy.released = form.cleaned_data['released']
                taxonomy.version = form.cleaned_data['version']
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
            return redirect('pcs.primcom.views.add')
        else:
            context['form'] = TraitDataForm(request.POST)
    else:
        context['form'] = TraitDataForm()

    # The initial "add" page
    context['auto_fields'] = _get_auto_fields(context['form'])
    context['add_active'] = True
    return render_to_response('primcom/traitdata_form.html', context,
                              context_instance=RequestContext(request))
