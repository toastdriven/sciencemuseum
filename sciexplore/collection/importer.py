import models as m

def strip_or_none(s):
    if s is not None:
        return s.strip() or None
    return None

def do_import(et):
    for el in et.findall('.//MuseumObject'):
        text = lambda tag: strip_or_none(el.find(tag).text)
        
        # Sort out the image
        image = None
        img_el = el.find('Image')
        if img_el.find('Id') is not None:
            image, created = m.Image.objects.get_or_create(
                xml_id = img_el.find('Id').text.strip(),
                defaults = {
                    'credit': strip_or_none(img_el.find('Credit').text),
                    'source': strip_or_none(img_el.find('Source').text),
                }
            )
        
        lookup_args = {
            'accession_number': text('AccessionNumber'),
        }
        create_args = {
            'name': text('Name'),
            'period_name': text('PeriodName'),
            'permanent_uri': text('PermanentURI'),
            'text': text('Text'),
            'year_made': text('YearMade'),
            'credit': text('Credit'),
            'headline': text('Headline'),
            'interpretative_date': text('InterpretativeDate'),
            'interpretative_place': text('InterpretativePlace'),
            'made_date_end': text('MadeDateEnd'),
            'made_date_start': text('MadeDateStart'),
            'image': image,
        }
        kwargs = dict(lookup_args)
        kwargs['defaults'] = create_args
        obj, created = m.MuseumObject.objects.get_or_create(**kwargs)
        
        # Now the many-to-many fields, which are a bit more tricky
        
        for child in el.findall('.//LinkedCelestialBodies/CelestialBody'):
            body, created = m.CelestialBody.objects.get_or_create(
                common_name = child.find('CommonName').text.strip(),
                defaults = {
                    'astronomical_name': strip_or_none(
                        child.find('AstronomicalName').text
                    ),
                    'alternative_name': strip_or_none(
                        child.find('AlternativeName').text
                    ),
                }
            )
            obj.celestial_bodies.add(body)
        
        for child in el.findall('.//LinkedPeople/Person'):
            person, created = m.Person.objects.get_or_create(
                xml_id = child.find('Id').text.strip(),
                defaults = {'name': child.find('Name').text.strip()}
            )
            obj.linked_people.create(
                person = person,
                relationship = child.find('Relationship').text,
            )
        
        for child in el.findall('.//LinkedPlaces/Place'):
            place, created = m.Place.objects.get_or_create(
                xml_id = child.find('Id').text.strip(),
                defaults = {'place_name':child.find('PlaceName').text.strip()}
            )
            obj.linked_places.create(
                place = place,
                relationship = child.find('Relationship').text,
            )
        
        for child in el.findall('MultiMediaItems/Multimedia'):
            multimedia, created = m.Multimedia.objects.get_or_create(
                xml_id = child.find('Id').text.strip(),
                defaults = {
                    'name': strip_or_none(child.find('Name').text),
                    'source_file': strip_or_none(
                        child.find('SourceFile').text
                    ),
                    'type': strip_or_none(
                        child.find('Type').text
                    ),
                    'xml_source': strip_or_none(
                        child.find('XmlSource').text
                    ),
                }
            )
            obj.multi_media_items.add(multimedia)
        
        # If it has a PlaceMade, set that up now
        if el.find('PlaceMade/Id') is not None:
            place_made, created = m.Place.objects.get_or_create(
                xml_id = el.find('PlaceMade/Id').text.strip(),
                defaults = {
                    'place_name': el.find('PlaceMade/PlaceName').text.strip(),
                }
            )
            linked_place = m.LinkedPlace.objects.create(
                place = place_made,
                museum_object = obj,
                relationship = el.find('PlaceMade/Relationship').text
            )
            obj.place_made = linked_place
            obj.save()
