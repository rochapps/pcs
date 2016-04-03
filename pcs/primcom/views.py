import codecs
import datetime
import pprint

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from .models import TraitData, Trait, Taxonomy, Location, Reference
from .forms import QueryDataForm
from .utils import write_raw_data_file, write_mean_data_file


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
    qs = TraitData.objects.all().filter(trait__in=traits).filter(taxonomy__pk__in=species
          ).order_by('taxonomy__species_reported_name', 'trait__name', 'sex').select_related('trait', 'taxonomy')
    # Add the Excel BOM for UTF-8 encoding
    response.write(codecs.BOM_UTF8)
    # write_mean_data_file(response, qs, traits, taxonomy)
    write_raw_data_file(response, qs, traits, taxonomy)
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
