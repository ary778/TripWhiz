# In api/urls.py

from django.urls import path
from .views import DealListView

urlpatterns = [
    path('deals/', DealListView.as_view(), name='deal-list'),
]