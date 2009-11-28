from django.core.management.base import BaseCommand, CommandError
from xml.etree import ElementTree as ET
from collection import importer
import urllib

class Command(BaseCommand):
    help = "Import science museum API XML"
    
    requires_model_validation = True
    can_import_settings = True
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Command accepts one argument")
        url = args[0]
        if url.startswith('http://'):
            fp = urllib.urlopen(url)
        else:
            fp = open(url)
        et = ET.parse(fp)
        importer.do_import(et)
        print "Import complete"
