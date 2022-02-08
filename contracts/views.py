#Django
from os.path import join
from django.conf import settings
from django.shortcuts import render, redirect
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
        contract = ContractForm(request.POST, request.FILES)
        instance = contract.save()

        dataset = Dataset()
        path = join(settings.MEDIA_ROOT, str(instance.archivo))
        imported_data = dataset.load(open(path, 'rb').read(), format='xlsx')

        for data in imported_data:
            rate = Rates()
            if data[0] is None:
                break
            rate.origin = data[0]
            rate.destination = data[1]
            rate.currency = data[4]
            rate.twenty = data[5]
            rate.forty = data[6]
            rate.fortyhc = data[7]
            rate.contract = instance
            rate.save()

        return redirect('contract_new')
    return render(request, 'contracts/index.html', {'form': form})
