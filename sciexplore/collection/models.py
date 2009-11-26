from django.db import models

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
    
    def __unicode__(self):
        return self.common_name

class Person(models.Model):
    xml_id = models.CharField(unique = True, max_length = 20)
    name = models.CharField(max_length = 255)
    
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
    
    def __unicode__(self):
        return u'%s: %s' % (self.accession_number, self.name)

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
