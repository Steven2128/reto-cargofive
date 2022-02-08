#Django
from django import forms
#Models
from .models import Contracts


class ContractForm(forms.ModelForm):
    """Formulario base del modelo Contract"""
    class Meta:
        model = Contracts
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs= {'type': 'date'})
        }
