#Django
from os.path import join
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
#Models
from .models import Rates
#Forms
from .forms import ContractForm
#Tablib
from tablib import Dataset


def contract_view(request):
    """Vista para crear nuevos contratos"""
    form = ContractForm()
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            dataset = Dataset()
            path = join(settings.MEDIA_ROOT, str(instance.archivo))

            file = request.FILES['archivo']
            if file.name.endswith('xlsx'):
                imported_data = dataset.load(open(path, 'rb').read(), format="xlsx")
            elif file.name.endswith('csv'):
                imported_data = dataset.load(open(path, 'rt', encoding='utf8').read())
            elif file.name.endswith('xls'):
                imported_data = dataset.load(open(path, 'rb').read(), format="xls")
            for data in imported_data:
                rate = Rates()
                if data[0] and data[1] and data[4] and data[5] and data[6] and data[7] is None:
                    continue
                rate.origin = data[0]
                rate.destination = data[1]
                rate.currency = data[4]
                rate.twenty = data[5]
                rate.forty = data[6]
                rate.fortyhc = data[7]
                rate.contract = instance
                rate.save()
            messages.success(request, 'Datos importados exitosamente!')
            return redirect('list_rates')
    return render(request, 'contracts/index.html', {'form': form})


class ListRateView(ListView):
    """Vista para mostrar todas las tarifas"""
    model = Rates
    template_name = 'contracts/list_rates.html'
    context_object_name = 'rates'

