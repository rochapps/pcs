'''Main URL configuration for the primcom application.'''

from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.home),
  url(r'^info$', views.info),
  url(r'^collaborators$', views.Collaborators.as_view()),
  url(r'^query$', views.query),
  url(r'^csv$', views.csv_data),
  url(r'^csv$', views.csv_data),
  url(r'^methods', views.methods),
  url(r'^archive$', views.archive),
  url(r'^contact$', views.contact),
  # The main "add" page
  url(r'^add$', views.add),
]
