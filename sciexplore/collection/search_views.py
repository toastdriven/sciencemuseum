from django import forms
from django.db import models
from haystack.forms import SearchForm, model_choices
from haystack.query import SearchQuerySet
from haystack.views import SearchView


MODEL_CHOICES = [
    ('', 'Everything'),
    ('collection.museumobject', 'Items'),
    ('collection.person', 'People'),
    ('collection.celestialbody', 'Celestial bodies'),
]


class ModelSearchForm(SearchForm):
    what = forms.ChoiceField(choices=MODEL_CHOICES, required=False, label='Search In', widget=forms.Select)
    
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


class MySearchView(SearchView):
    def __init__(self, *args, **kwargs):
        kwargs['form_class'] = ModelSearchForm
        super(MySearchView, self).__init__(*args, **kwargs)
    
    def extra_context(self):
        q = self.get_query()
        if q:
            return {
                'suggestion': SearchQuerySet().spelling_suggestion(q),
            }
        else:
            return {}
