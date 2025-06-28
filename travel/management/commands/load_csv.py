import csv
from django.utils import timezone
from datetime import datetime
from django.core.management.base import BaseCommand
from travel.models import TravelOption

class Command(BaseCommand):
    help = 'Load data from travel_data_progress.csv'

    def handle(self, *args, **kwargs):
        with open('travel_data_progress.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                TravelOption.objects.create(
                    origin=row['Origin'],
                    iata=row['IATA'],
                    city=row['City'],
                    flight_price=float(row['Flight_Price(INR)']) if row['Flight_Price(INR)'] else None,
                    hotel_price=float(row['Hotel_Price(INR)']) if row['Hotel_Price(INR)'] else None,
                    check_in=row['Check_In'],
                    check_out=row['Check_Out'],
                    scraped_at=timezone.make_aware(datetime.strptime(row['Scraped_At'], "%Y-%m-%d %H:%M:%S")),
                    type=row['Type']
                )
        self.stdout.write(self.style.SUCCESS("✅ CSV data loaded!"))
