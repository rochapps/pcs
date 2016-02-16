'''Main URL configuration for the primcom application.'''

from django.conf.urls import patterns


urlpatterns = patterns(
  'primcom.views',
  (r'^$', 'home'),
  (r'^info$', 'info'),
  (r'^collaborators$', 'collaborators'),
  (r'^query$', 'query'),
  (r'^csv$', 'csv_data'),
  (r'^methods', 'methods'),
  (r'^archive$', 'archive'),
  (r'^contact$', 'contact'),

  # The main "add" page
  (r'^add$', 'add'),
)
