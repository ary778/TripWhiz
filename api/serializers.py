import requests
from django.conf import settings
from rest_framework import serializers
from travel.models import Deal, Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['name', 'iata_code', 'category']

class DealSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = [
            'id', 'origin_name', 'origin_iata', 'destination', 
            'total_price', 'imageUrl'
        ]

    def get_imageUrl(self, obj):
        api_key = settings.PEXELS_API_KEY
        query = obj.destination.name
        placeholder = f"https://placehold.co/600x400/005A8D/FFFFFF?text={query.replace(' ', '%20')}"

        if not api_key:
            return placeholder

        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("photos") and len(data["photos"]) > 0:
                return data["photos"][0]["src"]["large"]
            else:
                return placeholder
        except requests.exceptions.RequestException as e:
            print(f"Pexels API request failed for '{query}': {e}")
            return placeholder