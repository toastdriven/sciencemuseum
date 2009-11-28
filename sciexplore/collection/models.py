from django.db import models
import re, sys

class Image(models.Model):
    credit = models.CharField(max_length = 255)
    xml_id = models.CharField(max_length = 100)
    source = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.xml_id

class CelestialBody(models.Model):
    common_name = models.CharField(max_length=100, unique=True)
    alternative_name = models.CharField(max_length=100, blank=True,null=True)
    astronomical_name = models.CharField(max_length=100, blank=True,null=True)
    
    def get_absolute_url(self):
        return u'/celestial-body/%s/' % self.pk
    
    def __unicode__(self):
        return self.common_name

class Person(models.Model):
    xml_id = models.CharField(unique = True, max_length = 20)
    name = models.CharField(max_length = 255)
    
    def items(self):
        "Returns items with their relationship types"
        items = {}
        for link in self.linkedperson_set.select_related('museum_object'):
            items.setdefault(link.museum_object, []).append(link.relationship)
        pairs = items.items()
        # Sort by first 4 digits of interpretative_date, which should be year
        pairs.sort(
            key = lambda p: p[0].guess_year() or 3000
        )
        return pairs
    
    def related_people(self):
        return Person.objects.filter(
            linkedperson__museum_object__linked_people__person = self
        ).exclude(pk = self.pk).distinct()
    
    def get_absolute_url(self):
        return u'/person/%s/' % self.pk
    
    def __unicode__(self):
        return self.name

class LinkedPerson(models.Model):
    person = models.ForeignKey(Person)
    museum_object = models.ForeignKey('MuseumObject', 
        related_name = 'linked_people'
    )
    relationship = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return u'%s: %s: %s' % (
            self.person, self.relationship, self.museum_object
        )

class Place(models.Model):
    xml_id = models.CharField(unique = True, max_length = 20)
    place_name = models.CharField(max_length = 255)
    
    def short(self):
        return ','.join(self.place_name.split(',')[:3])
    
    def __unicode__(self):
        return self.place_name

class LinkedPlace(models.Model):
    place = models.ForeignKey(Place)
    museum_object = models.ForeignKey('MuseumObject',
        related_name='linked_places'
    )
    relationship = models.CharField(max_length = 100)
    
    def __unicode__(self):
        return u'%s: %s: %s' % (
            self.place, self.relationship, self.museum_object
        )

class Multimedia(models.Model):
    xml_id = models.CharField(unique = True, max_length = 20)
    name = models.CharField(max_length = 255, null=True, blank=True)
    source_file = models.CharField(max_length = 255, null=True, blank=True)
    type = models.CharField(max_length = 255, null=True, blank=True)
    xml_source = models.CharField(max_length = 255, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class MuseumObject(models.Model):
    accession_number = models.CharField(unique=True, max_length=100)
    credit = models.CharField(max_length = 255)
    headline = models.CharField(max_length = 255, null=True, blank=True)
    image = models.ForeignKey(Image, blank = True, null = True)
    interpretative_date = models.CharField(
        max_length = 255, null=True, blank=True
    )
    interpretative_place = models.CharField(
        max_length = 255, null=True, blank=True
    )
    celestial_bodies = models.ManyToManyField(
        CelestialBody, null=True, blank=True
    )
    made_date_end = models.CharField(max_length = 100, null=True, blank=True)
    made_date_start = models.CharField(max_length =100, null=True, blank=True)
    multi_media_items = models.ManyToManyField(
        Multimedia, null=True, blank=True
    )
    name = models.CharField(max_length = 255)
    period_name = models.CharField(max_length = 255, null=True)
    permanent_uri = models.CharField(max_length = 255)
    place_made = models.ForeignKey(LinkedPlace, null=True, 
        related_name='manufactured_here'
    )
    text = models.TextField()
    year_made = models.CharField(max_length = 255, null=True)
    
    year_re = re.compile('(\d{3,4})')
    
    class Meta:
        verbose_name = 'Item'
    
    def people(self):
        "Returns people with their relationship types"
        people = {}
        for link in self.linked_people.select_related('person'):
            people.setdefault(link.person, []).append(link.relationship)
        return people.items()
    
    def places(self):
        "Returns places with their relationship types"
        places = {}
        for link in self.linked_places.select_related('person'):
            places.setdefault(
                link.place.short(), []
            ).append(link.relationship)
        return places.items()
    
    def related_objects(self):
        # Related objects share a person, place or celestial 
        # body. We order based on a simple scoring mechanism.
        same_person = MuseumObject.objects.filter(
            linked_people__person__linkedperson__museum_object = self
        ).exclude(pk = self.pk).distinct()
        
        same_place = MuseumObject.objects.filter(
            linked_places__place__linkedplace__museum_object = self
        ).exclude(pk = self.pk).distinct()
        
        same_celestial_body = MuseumObject.objects.filter(
            celestial_bodies__in = self.celestial_bodies.all()
        ).exclude(pk = self.pk).distinct()
        
        results = {}
        
        for obj in same_person:
            results[obj] = results.get(obj, 0) + 5
        for obj in same_place:
            results[obj] = results.get(obj, 0) + 2
        for obj in same_celestial_body:
            results[obj] = results.get(obj, 0) + 1
        
        results = results.items()
        results.sort(key = lambda p: p[1], reverse=True)
        return results
    
    def guess_year(self):
        "Assumes first 4 digits are the year"
        s = self.interpretative_date or ''
        match = self.year_re.search(s)
        if match:
            return int(match.group(1))
        return None
    
    def get_absolute_url(self):
        return u'/item/%s/' % self.accession_number
    
    def image_size(self, size):
        if self.image and self.image.source:
            return (
                'http://www.sciencemuseum.org.uk' +
                self.image.source.replace('size=Medium', 'size=%s' % size)
            )
        return None
    
    def image_small(self):
        return self.image_size('Small')
    
    def image_inline(self):
        return self.image_size('Inline')
    
    def image_medium(self):
        return self.image_size('Medium')
    
    def image_large(self):
        return self.image_size('Large')
    
    def __unicode__(self):
        return u'%s: %s (%s)' % (
            self.interpretative_date, 
            self.name,
            self.accession_number
        )

class Material(models.Model):
    museum_object = models.ForeignKey(MuseumObject, related_name='materials')
    component = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s of %s' % (self.component, self.museum_object)

class Measurement(models.Model):
    museum_object =models.ForeignKey(MuseumObject,related_name='measurements')
    part_measured = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s of %s' % (self.part_measured, self.museum_object)
