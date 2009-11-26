from haystack import indexes
from haystack import site
from models import MuseumObject, Person, CelestialBody

class MuseumObjectIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='text')
    def get_queryset(self):
        return MuseumObject.objects.all()

site.register(MuseumObject, MuseumObjectIndex)

class PersonIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='name')    
    def get_queryset(self):
        return Person.objects.all()

site.register(Person, PersonIndex)

class CelestialBodyIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='common_name')    
    def get_queryset(self):
        return CelestialBody.objects.all()

site.register(CelestialBody, CelestialBodyIndex)
