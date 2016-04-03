from django.contrib import admin
from .models import Reference, Taxonomy, Location, TraitData, Trait


admin.site.register(Reference)
admin.site.register(Taxonomy)
admin.site.register(Location)
admin.site.register(TraitData)
admin.site.register(Trait)
