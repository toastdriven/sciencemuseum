from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from collection import models
for name in dir(models):
    print name
    if name[0].upper() == name[0] and name[0] != '_':
        obj = getattr(models, name, None)
        if obj and issubclass(obj, models.models.Model):
            databrowse.site.register(obj)

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),

)
