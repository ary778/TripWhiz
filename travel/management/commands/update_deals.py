# In travel/management/commands/update_deals.py

import json
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from serpapi import GoogleSearch
from travel.models import Destination, Deal

# --- Configuration ---
ORIGINS = [
    {"name": "Ahmedabad", "iata": "AMD"},
    {"name": "Mumbai", "iata": "BOM"},
    {"name": "Delhi", "iata": "DEL"},
]

class Command(BaseCommand):
    help = 'Fetches flight and hotel prices to create or update deals in the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting the deal update process...'))

        start_date = date.today() + timedelta(days=90)
        end_date = start_date + timedelta(days=5)
        
        outbound_date_str = start_date.strftime("%Y-%m-%d")
        return_date_str = end_date.strftime("%Y-%m-%d")
        check_out_date_str = end_date.strftime("%Y-%m-%d")

        destinations = Destination.objects.all()
        if not destinations:
            self.stdout.write(self.style.WARNING('No destinations found. Please load destinations first.'))
            return

        for origin in ORIGINS:
            for destination in destinations:
                if origin['iata'] == destination.iata_code:
                    continue

                self.stdout.write(f"🔍 Checking route: {origin['name']} ({origin['iata']}) -> {destination.name} ({destination.iata_code})")

                try:
                    # --- Fetch Lowest Flight Price ---
                    flight_params = {
                        "engine": "google_flights",
                        "api_key": settings.SERPAPI_FLIGHTS_API_KEY,
                        "departure_id": origin['iata'],
                        "arrival_id": destination.iata_code,
                        "outbound_date": outbound_date_str,
                        "return_date": return_date_str,
                        "currency": "INR", "hl": "en"
                    }
                    flight_search = GoogleSearch(flight_params)
                    flight_results = flight_search.get_dict()
                    
                    flight_price = flight_results.get("price_insights", {}).get("lowest_price")
                    if not flight_price and flight_results.get("best_flights"):
                        flight_price = flight_results["best_flights"][0].get("price")

                    if not flight_price:
                        self.stdout.write(self.style.WARNING(f"   - No flight price found for {origin['iata']}->{destination.iata_code}"))
                        continue

                    # --- Fetch Hotel Price ---
                    hotel_params = {
                        "engine": "google_hotels",
                        "api_key": settings.SERPAPI_HOTELS_API_KEY,
                        "q": f"hotel in {destination.name}",
                        "check_in_date": outbound_date_str,
                        "check_out_date": check_out_date_str,
                        "currency": "INR", "hl": "en"
                    }
                    hotel_search = GoogleSearch(hotel_params)
                    hotel_results = hotel_search.get_dict()

                    hotel_price_per_night = None
                    
                    # --- FIX: Check the "ads" key instead of "properties" ---
                    hotel_list = hotel_results.get("ads")
                    if hotel_list:
                        # Get the price from the first hotel in the "ads" list
                        # and use the "extracted_price" field.
                        hotel_price_per_night = hotel_list[0].get("extracted_price")
                    # --- END FIX ---
                    
                    if not hotel_price_per_night:
                        self.stdout.write(self.style.WARNING(f"   - No hotel price found for {destination.name}"))
                        continue

                    # --- Calculate Total and Save Deal ---
                    total_hotel_price = hotel_price_per_night * 5
                    total_deal_price = flight_price + total_hotel_price

                    deal, created = Deal.objects.update_or_create(
                        origin_iata=origin['iata'],
                        destination=destination,
                        defaults={
                            'origin_name': origin['name'],
                            'flight_price': flight_price,
                            'hotel_price': total_hotel_price,
                            'total_price': total_deal_price,
                            'category': destination.category,
                        }
                    )

                    status = "CREATED" if created else "UPDATED"
                    self.stdout.write(self.style.SUCCESS(f"   ✅ Deal {status}: Total Price ${total_deal_price}"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ❌ An error occurred: {e}"))

        self.stdout.write(self.style.SUCCESS('\n🎉 Deal update process complete!'))