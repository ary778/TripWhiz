# In travel/management/commands/fetch_images.py
import requests
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from travel.models import Destination # UPDATED: Use the new Destination model

class Command(BaseCommand):
    help = "Fetches city images from Pexels API and updates Destination models"

    def handle(self, *args, **kwargs):
        # --- Security Improvement: Get API key from settings ---
        # This is safer than hard-coding it in the file.
        # See instructions below on how to set this up.
        pexels_api_key = getattr(settings, 'PEXELS_API_KEY', None)
        if not pexels_api_key:
            self.stdout.write(self.style.ERROR("PEXELS_API_KEY not found in settings.py"))
            return
            
        headers = {"Authorization": pexels_api_key}

        # UPDATED: Loop through Destination objects instead of TravelOption
        for destination in Destination.objects.all():
            if not destination.image_url:
                query = destination.name # UPDATED: Use destination.name for the query
                
                self.stdout.write(f"Searching for image of {destination.name}...")
                response = requests.get(
                    f"https://api.pexels.com/v1/search?query={query}&per_page=1",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("photos"):
                        image_url = data["photos"][0]["src"]["large"] # Use "large" for better quality
                        destination.image_url = image_url # UPDATED
                        destination.save() # UPDATED
                        self.stdout.write(self.style.SUCCESS(f"✔ Updated image for {destination.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"⚠ No image found for {destination.name}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Error fetching image for {destination.name}: {response.status_code}"))