import codecs
import datetime
import os
import pprint
import shutil
from time import time

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from .models import TraitData, Trait, Taxonomy, Location, Reference
from .forms import QueryDataForm
from .utils import write_raw_data_file, write_mean_data_file, write_location_data_file, write_location_references_file


def _get_auto_fields(form):
    auto_fields = []
    for trait in Trait.objects.order_by('category', 'name'):
        trait_fields = []
        trait_fields.append(trait.name)
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

    # Handle form processing
    # form = QueryDataForm(request.POST)

    # The 'taxonomy' field determines Trait names
    taxonomy_choice = request.POST.get('taxonomy', None)
    if taxonomy_choice == 'species_raw':
        taxonomy = 'raw'
    elif taxonomy_choice == 'species_wr':
        taxonomy = 'wr'
    elif taxonomy_choice == 'species_ch':
        taxonomy = 'ch'
    else:
        taxonomy = 'raw'
    species = request.POST.getlist(taxonomy_choice)
    print("Species:")
    pprint.pprint(species)
    traits = request.POST.getlist('traits')
    print("Traits:")
    pprint.pprint(traits)

    for q in request.POST:
        print("{0} == {1}".format(q, request.POST.getlist(q)))

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response_filename = 'pcs_results-{0}.csv'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    response['Content-Disposition'] = 'attachment; ' \
                                      'filename={0}'.format(response_filename)
    traits = Trait.objects.in_bulk(traits)
    locations = Location.objects.all()
    references = Reference.objects.all()
    qs = TraitData.objects.all().filter(trait__in=traits).filter(taxonomy__pk__in=species
          ).order_by('taxonomy__species_reported_name', 'trait__name', 'sex').select_related('trait', 'taxonomy')
    # Add the Excel BOM for UTF-8 encoding
    response.write(codecs.BOM_UTF8)
    # make a directory for current download
    now = str(time()).replace('.', '')
    tempdir = os.path.join(settings.MEDIA_ROOT, 'downloads', now)
    os.mkdir(tempdir)
    # create files to be downloaded
    write_mean_data_file(os.path.join(tempdir, 'mean_values.csv'), qs, traits, taxonomy)
    write_raw_data_file(os.path.join(tempdir, 'raw_data.csv'), qs, traits, taxonomy)
    write_location_data_file(os.path.join(tempdir, 'locations.csv'), locations)
    write_location_references_file(os.path.join(tempdir, 'references.csv'), references)
    # zip all files we created
    zip_file_name = shutil.make_archive(os.path.join(settings.MEDIA_ROOT, 'downloads', "pcs_{0}".format(now)), 'zip', tempdir)
    # remove created files
    shutil.rmtree(tempdir)
    # open zipfile
    zip_file = open(os.path.join(tempdir, zip_file_name), 'rb')
    # transmit zipfile in 8KB chunks
    wrapper = FileWrapper(zip_file)
    response = StreamingHttpResponse(wrapper, content_type='application/zip')
    response['Content-Length'] = zip_file.tell()
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(zip_file_name)
    zip_file.seek(0)
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
