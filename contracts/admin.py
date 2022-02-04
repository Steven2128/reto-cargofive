#Django
from django.contrib import admin
#Models
from .models import Contracts, Rates

admin.site.register(Contracts)
admin.site.register(Rates)
