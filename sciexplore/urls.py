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


from haystack.forms import SearchForm, model_choices
from django import forms
from django.db import models
class ModelSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)
        self.fields['what'] = forms.ChoiceField(
            choices = [
                ('', 'Everything'),
                ('collection.museumobject', 'Items'),
                ('collection.person', 'People'),
                ('collection.celestialbody', 'Celestial bodies'),
            ],
            required=False,
            label='Search In',
            widget=forms.Select
        )

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.cleaned_data['what']:
            model = self.cleaned_data['what']
            search_models.append(models.get_model(*model.split('.')))

        return search_models

    def search(self):
        sqs = super(ModelSearchForm, self).search()
        return sqs.models(*self.get_models())

from haystack.views import SearchView

urlpatterns = patterns('',
    (r'^item/$', 'collection.views.all'),
    (r'^item/(.*)/$', 'collection.views.item'),
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    
    (r'^search/$', SearchView(form_class = ModelSearchForm)),
)
