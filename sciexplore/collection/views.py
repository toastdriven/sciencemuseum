from django.shortcuts import render_to_response as render, get_object_or_404
from django.conf import settings
from django.db.models import Count
import models as m
from search_views import ModelSearchForm

def index(self):
    return render('index.html', {
        'num_items': m.MuseumObject.objects.count(),
        'num_people': m.Person.objects.count(),
        'num_celestial_bodies': m.CelestialBody.objects.count(),
        'form': ModelSearchForm(),
    })

def all(self):
    return render('all.html', {
        'items': m.MuseumObject.objects.all(),
    })

def item(self, acnum):
    return render('item.html', {
        'item': get_object_or_404(m.MuseumObject, accession_number = acnum),
        'maps_api_key': settings.MAPS_API_KEY
    })

def person(self, pk):
    return render('person.html', {
        'person': get_object_or_404(m.Person, pk = pk),
    })

def celestial_body(self, pk):
    return render('celestial_body.html', {
        'body': get_object_or_404(m.CelestialBody, pk = pk),
    })

def all_people(self):
    return render('all_people.html', {
        'people': m.Person.objects.annotate(
            num = Count('linkedperson__museum_object', distinct=True)
        ).order_by('-num'),
    })

def all_celestial_bodies(self):
    return render('all_celestial_bodies.html', {
        'bodies': m.CelestialBody.objects.annotate(
            num = Count('museumobject')
        ).order_by('-num')
    })
