from django.shortcuts import render
from .models import TravelOption

def home(request):
    return render(request, 'travel/budget_form.html')

def results(request):
    budget = request.GET.get("budget")
    trips = []

    if budget:
        budget = float(budget)
        all_options = TravelOption.objects.filter(
            flight_price__isnull=False,
            hotel_price__isnull=False
        )
        seen = set()
        for option in sorted(all_options, key=lambda x: x.total_price()):
            if option.city not in seen and option.total_price() <= budget:
                trips.append(option)
                seen.add(option.city)

    return render(request, 'travel/results.html', {"results": trips, "budget": budget})
