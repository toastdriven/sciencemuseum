from django.conf.urls.defaults import *
from django.conf import settings
import os

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from collection import models
for name in dir(models):
    if name[0].upper() == name[0] and name[0] != '_':
        obj = getattr(models, name, None)
        if obj and issubclass(obj, models.models.Model):
            databrowse.site.register(obj)

from collection.search_views import MySearchView

item_options = {
    'queryset': models.MuseumObject.objects.all(),
    'template_name': 'all.html',
    'paginate_by': 20,
}

urlpatterns = patterns('',
    (r'^$', 'collection.views.index'),
    (r'^items/$',
        'django.views.generic.list_detail.object_list', item_options
    ),
    (r'^items/page(?P<page>[0-9]+)/$', 
        'django.views.generic.list_detail.object_list', item_options
    ),
    (r'^item/(.*)/$', 'collection.views.item'),
    (r'^item/$', 'django.views.generic.simple.redirect_to', {
        'url': '/items/',
    }),
    
    (r'^people/$', 'collection.views.all_people'),
    (r'^person/(\d+)/$', 'collection.views.person'),
    (r'^person/$', 'django.views.generic.simple.redirect_to', {
        'url': '/people/',
    }),
    
    (r'^celestial-bodies/$', 'collection.views.all_celestial_bodies'),
    (r'^celestial-body/(\d+)/$', 'collection.views.celestial_body'),
    (r'^celestial-body/$', 'django.views.generic.simple.redirect_to', {
        'url': '/celestial-bodies/',
    }),
    
    # (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    
    (r'^search/$', MySearchView()),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.OUR_ROOT, 'static'),
    }),
)
