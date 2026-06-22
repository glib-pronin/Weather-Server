from django.core.management.base import BaseCommand
from pathlib import Path
from babel import Locale
import json, pycountry



class Command(BaseCommand):
    def handle(self, *args, **options):
        locale = Locale('uk')

        data = [
            {
                'name': locale.territories.get(c.alpha_2),
                'code': c.alpha_2
            }
            for c in pycountry.countries
        ]

        path = Path(__file__).resolve().parent.parent.parent / 'data' / 'countries.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        self.stdout.write('File created')