import requests
from django.core.management.base import BaseCommand
from travel.models import TravelOption

API_KEY = "LnWxrtJb7sHkgGDNh8HnoE9TkyZSnzbrKqEnrFjsQoB16pHW3e9WLkZB"
HEADERS = {"Authorization": API_KEY}

class Command(BaseCommand):
    help = "Fetch city images from Pexels API and update TravelOption models"

    def handle(self, *args, **kwargs):
        for option in TravelOption.objects.all():
            if not option.image_url:
                query = option.city
                response = requests.get(
                    f"https://api.pexels.com/v1/search?query={query}&per_page=1",
                    headers=HEADERS
                )
                data = response.json()
                if data.get("photos"):
                    image_url = data["photos"][0]["src"]["medium"]
                    option.image_url = image_url
                    option.save()
                    self.stdout.write(self.style.SUCCESS(f"✔ Updated image for {option.city}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠ No image found for {option.city}"))
