#Django
from django import forms
from django.core.validators import FileExtensionValidator
#Models
from .models import Contracts


class ContractForm(forms.ModelForm):
    """Formulario base del modelo Contract"""
    archivo = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['csv', 'xls', 'xlsx'])])
    class Meta:
        model = Contracts
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs= {'type': 'date'}),
        }
