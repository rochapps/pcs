from django.contrib import admin
from .models import Reference, Taxonomy, Location, TraitData


admin.site.register(Reference)
admin.site.register(Taxonomy)
admin.site.register(Location)
admin.site.register(TraitData)
