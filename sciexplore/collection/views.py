from django.shortcuts import render_to_response as render, get_object_or_404
from django.conf import settings
import models as m

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
        'people': m.Person.objects.all(),
    })

def all_celestial_bodies(self):
    return render('all_celestial_bodies.html', {
        'bodies': m.CelestialBody.objects.all(),
    })
