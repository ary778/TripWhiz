from django.contrib import admin
from .models import TravelOption

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('city', 'iata', 'origin', 'flight_price', 'hotel_price', 'check_in', 'check_out')
    list_filter = ('check_in', 'check_out')  # or remove if not needed
