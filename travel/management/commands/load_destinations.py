import json
from django.core.management.base import BaseCommand
from travel.models import Destination

class Command(BaseCommand):
    help = 'Loads destinations from a destinations.json file into the database'

    def handle(self, *args, **kwargs):
        # First, clear all existing destinations to avoid duplicates
        self.stdout.write(self.style.WARNING('Clearing old destination data...'))
        Destination.objects.all().delete()

        try:
            with open('destinations.json', 'r') as f:
                destinations = json.load(f)

            self.stdout.write("Loading new destinations into the database...")
            
            count = 0
            for item in destinations:
                Destination.objects.create(
                    name=item['city'],
                    iata_code=item['iata_code'],
                    category=item['category']
                    # The hotel_query is not part of your Destination model, 
                    # so we don't load it here. The update_deals command
                    # will construct the query.
                )
                count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} destinations.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('Error: destinations.json not found in the root directory.'))
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f'Error: Missing key {e} in a JSON object.'))