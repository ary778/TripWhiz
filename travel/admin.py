# In travel/admin.py
from django.contrib import admin
from .models import Destination, Deal

admin.site.register(Destination)
admin.site.register(Deal)