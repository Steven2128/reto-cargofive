#Django
from django.db import models


class Contracts(models.Model):
    """Modelo Contracts para guardar los contratos"""
    nombre = models.CharField("Nombre del contrato", max_length=150, blank=False, null=False)
    fecha = models.DateField("Fecha del contrato", auto_now=False, auto_now_add=False)
    archivo = models.FileField("Archivo", upload_to='contracts/')

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        return self.nombre



class Rates(models.Model):
    """Modelo Rates para guardar los costos de viajes"""
    origin = models.CharField("Puerto de origen", max_length=150, blank=False, null=False)
    destination = models.CharField("Puerto de dstino", max_length=150, blank=False, null=False)
    currency = models.CharField("Moneda", max_length=150, blank=False, null=False)
    twenty = models.CharField("20’GP", max_length=150, blank=False, null=False)
    forty = models.CharField("40’GP", max_length=150, blank=False, null=False)
    fortyhc = models.CharField("40’HC", max_length=150, blank=False, null=False)
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE, related_name='Contrato')

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"

    def __str__(self):
        return self.origin+' - '+self.destination
