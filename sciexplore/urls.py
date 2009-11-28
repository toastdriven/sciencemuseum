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
    (r'^items/$',
        'django.views.generic.list_detail.object_list', item_options
    ),
    (r'^items/page(?P<page>[0-9]+)/$', 
        'django.views.generic.list_detail.object_list', item_options
    ),
    (r'^item/(.*)/$', 'collection.views.item'),
    
    (r'^people/$', 'collection.views.all_people'),
    (r'^person/(\d+)/$', 'collection.views.person'),
    
    (r'^celestial-bodies/$', 'collection.views.all_celestial_bodies'),
    (r'^celestial-body/(\d+)/$', 'collection.views.celestial_body'),
    
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    
    (r'^search/$', MySearchView()),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.OUR_ROOT, 'static'),
    }),
)
