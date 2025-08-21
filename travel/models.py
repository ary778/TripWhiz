# In travel/models.py
from django.db import models

class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('BEACH', 'Beach'),
        ('MOUNTAIN', 'Mountain'),
        ('HISTORIC', 'Historic'),
    ]
    name = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Deal(models.Model):
    origin_name = models.CharField(max_length=100) # This field was missing
    origin_iata = models.CharField(max_length=10)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    flight_price = models.IntegerField()
    hotel_price = models.IntegerField()
    total_price = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=10, default='BEACH') # This field was missing

    class Meta:
        unique_together = ('origin_iata', 'destination')

    def __str__(self):
        return f"{self.origin_name} to {self.destination.name} for {self.total_price}"