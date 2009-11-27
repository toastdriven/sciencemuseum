from django.shortcuts import render_to_response as render, get_object_or_404
import models as m

def all(self):
    return render('all.html', {
        'items': m.MuseumObject.objects.all(),
    })

def item(self, acnum):
    return render('item.html', {
        'item': get_object_or_404(m.MuseumObject, accession_number = acnum),
    })

def person(self, pk):
    return render('person.html', {
        'person': get_object_or_404(m.Person, pk = pk),
    })

def celestial_body(self, pk):
    return render('celestial_body.html', {
        'body': get_object_or_404(m.CelestialBody, pk = pk),
    })
