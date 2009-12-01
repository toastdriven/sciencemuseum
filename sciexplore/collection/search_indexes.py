from haystack import indexes
from haystack import site
from collection.models import MuseumObject, Person, CelestialBody


class MuseumObjectIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')


class PersonIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')


class CelestialBodyIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='common_name')


site.register(MuseumObject, MuseumObjectIndex)
site.register(Person, PersonIndex)
site.register(CelestialBody, CelestialBodyIndex)
