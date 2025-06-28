from django.db import models

class TravelOption(models.Model):
    origin = models.CharField(max_length=10)
    iata = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    flight_price = models.FloatField(null=True, blank=True)
    hotel_price = models.FloatField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    check_in = models.DateField()
    check_out = models.DateField()
    scraped_at = models.DateTimeField()

    def total_price(self):
        return (self.flight_price or 0) + (self.hotel_price or 0)

    def __str__(self):
        return f"{self.city} ({self.iata})"
