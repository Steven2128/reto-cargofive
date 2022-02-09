#Django
from os.path import join
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
#Models
from .models import Rates, Contracts
#Forms
from .forms import ContractForm
#Tablib
from tablib import Dataset
#Pandas
import pandas as pd
import numpy as np


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
            #Verifica que extención es el archivo y realiza el corresondiente import
            if file.name.endswith('xlsx'):
                imported_data = dataset.load(open(path, 'rb').read(), format="xlsx")
            elif file.name.endswith('csv'):
                imported_data = dataset.load(open(path, 'rt', encoding='utf8').read())
            elif file.name.endswith('xls'):
                imported_data = dataset.load(open(path, 'rb').read(), format="xls")
            for data in imported_data:
                rate = Rates()
                if data[0] is None or data[1] is None or data[4] is None or data[5] is None or data[6] is None or data[7] is None:
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


def compare(request):
    """Vista para comparar las dos ultimas importaciones"""
    results = []
    if request.method == 'POST':
        #Se valida si hay por lo menos 2 registros de contratos
        if len(Contracts.objects.all().order_by('-id')[:2]) < 2:
            messages.error(request, 'Por favor agrege otro contrato para comparar')
        else:
            path1 = join(settings.MEDIA_ROOT, str(Contracts.objects.all().order_by('-id')[:2][0].archivo))
            path2 = join(settings.MEDIA_ROOT, str(Contracts.objects.all().order_by('-id')[:2][1].archivo))

            contract1 = pd.read_excel(path1)
            contract2 = pd.read_excel(path2)

            index = 0
            compare = []

            #Se hace la comparación con el archivo de mayor tamaño
            if len(contract1) >= len(contract2):
                max = contract1
                min = contract2
            else:
                max = contract2
                min = contract1
            for i in max.values:
                try:
                    compare.append(i == min.values[index])
                    if False in compare[index]:
                        results.append("Hay variación en la fila {}".format(index+2))
                except:
                    results.append("No hay fila {} en uno de los archivos".format(index+2))
                index += 1

            if len(results) == 0:
                results.append("Los dos ultimos archivos son identicos")

    return render(request, 'contracts/rates_compare.html', {'results': results})
