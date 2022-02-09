#Django
from django.urls import path
#Views
from .views import *

urlpatterns = [
    path('', contract_view, name='contract_new'),
    path('list/', ListRateView.as_view(), name='list_rates'),
    path('compare/', compare, name='compare_rate')
]