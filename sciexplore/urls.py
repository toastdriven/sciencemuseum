from django.conf.urls.defaults import *

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

urlpatterns = patterns('',
    (r'^item/$', 'collection.views.all'),
    (r'^item/(.*)/$', 'collection.views.item'),
    (r'^person/(\d+)/$', 'collection.views.person'),
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    
    (r'^search/$', MySearchView()),
)
