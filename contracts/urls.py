#Django
from django.urls import path
#Views
from .views import *

urlpatterns = [
    path('', contract_view, name='contract_new'),
]