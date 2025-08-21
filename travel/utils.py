import requests
import os
from datetime import date, timedelta
from .models import Deal, Destination

def get_trip_dates():
    """Calculates a 7-day trip starting 90 days from now."""
    today = date.today()
    outbound_date = today + timedelta(days=90)
    return_date = outbound_date + timedelta(days=7)
    return outbound_date.strftime("%Y-%m-%d"), return_date.strftime("%Y-%m-%d")

def fetch_and_store_deals_from_serpapi(source_iata, category):
    flights_api_key = os.getenv('SERPAPI_FLIGHTS_API_KEY')
    hotels_api_key = os.getenv('SERPAPI_HOTELS_API_KEY')
    
    if not flights_api_key or not hotels_api_key:
        print("ERROR: Missing Flights or Hotels API key in environment variables.")
        return False

    destinations_to_search = Destination.objects.all()
    if category:
        destinations_to_search = destinations_to_search.filter(category__iexact=category)
    
    print(f"\n--- Found {destinations_to_search.count()} destinations in your database for category: '{category or 'Any'}' ---")
    
    outbound_date_str, return_date_str = get_trip_dates()
    deals_created_count = 0

    for dest in destinations_to_search:
        if source_iata.upper() == dest.iata_code.upper():
            continue

        print(f"--- Searching prices for route: {source_iata} -> {dest.name} ---")
        flight_price, hotel_price = 0, 0

        # API Call for Flight Price (remains the same)
        try:
            flight_params = { "engine": "google_flights", "departure_id": source_iata, "arrival_id": dest.iata_code, "outbound_date": outbound_date_str, "return_date": return_date_str, "api_key": flights_api_key, "currency": "INR", "hl": "en" }
            response = requests.get("https://serpapi.com/search.json", params=flight_params, timeout=30)
            response.raise_for_status()
            results = response.json()
            flight_results = results.get("best_flights", []) + results.get("other_flights", [])
            if flight_results:
                flight_price = flight_results[0].get("price", 0)
                print(f"Found flight price: ₹{flight_price}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Flight API request failed for {dest.name}: {e}")

        # FINAL: Most robust API Call for Hotel Price
        try:
            # 1. Make the search query more specific
            hotel_q = f"{dest.name} city center hotels"
            hotel_params = { "engine": "google_hotels", "q": hotel_q, "check_in_date": outbound_date_str, "check_out_date": return_date_str, "adults": "2", "api_key": hotels_api_key, "currency": "INR", "hl": "en" }
            response = requests.get("https://serpapi.com/search.json", params=hotel_params, timeout=30)
            response.raise_for_status()
            results = response.json()
            
            # 2. Check for results in TWO possible locations in the response
            properties = results.get("properties") or results.get("all_prices")
            
            if properties:
                hotel_rates = [prop.get("rate") for prop in properties[:5] if prop.get("rate")]
                if hotel_rates:
                    average_nightly_rate = sum(hotel_rates) / len(hotel_rates)
                    hotel_price = int(average_nightly_rate * 7)
                    print(f"Found average hotel price: ₹{hotel_price} for 7 nights")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Hotel API request failed for {dest.name}: {e}")

        if flight_price == 0:
            print(f"No flight found for {dest.name}, skipping deal creation.")
            continue

        if hotel_price == 0:
            hotel_price = 35000
            print(f"Hotel price not found. Applying default price: ₹{hotel_price}")

        Deal.objects.create(
            origin_name=source_iata, origin_iata=source_iata,
            destination=dest, flight_price=flight_price, hotel_price=hotel_price,
            total_price=(flight_price + hotel_price)
        )
        deals_created_count += 1

    print(f"\n--- Finished. Created {deals_created_count} new deals. ---")
    return deals_created_count > 0