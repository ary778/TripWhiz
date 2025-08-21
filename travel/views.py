# In travel/views.py
from django.shortcuts import render
from .models import Deal, Destination # Correctly import the new models

def home_view(request):
    """
    This view gets all the pre-collected deals and destinations
    from the database and sends them to the homepage template.
    """
    deals = Deal.objects.order_by('total_price')
    destinations = Destination.objects.all()
    
    context = {
        'deals': deals,
        'destinations': destinations
    }
    
    # You will need to create a 'home.html' template to display this data
    return render(request, 'index.html', context)
def results_view(request):
    """
    Renders the results page.
    The actual search logic will be handled by your API and JavaScript for now.
    """
    return render(request, 'results.html')