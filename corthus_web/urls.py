from django.conf.urls import patterns, include, url
from settings import PROJECT_ROOT

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns(
    '',

#    (r'^folder/([a-z0-9_/-]+)', 'core.views.folder'),
#    (r'^chapter/([0-9]+)', 'corpus.views.chapter'),
    (r'^/?$',
     'core.views.index'),

    (r'^texts/([A-Za-z0-9_/,-]+)\.([a-z-]{2,20})$',
     'core.views.text'),

    (r'^texts/([A-Za-z0-9_/,-]+)\.([a-z-]{2,20})/correct$',
     'core.views.correct'),

    (r'^texts(/[A-Za-z0-9_/,-]*)$', # important: no dots allowed! (to prevent ../)
     'core.views.folder'),

    (r'^search',
     'core.views.search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
