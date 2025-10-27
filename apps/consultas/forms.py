#apps/consultas/forms.py:
from django import forms
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['data', 'horario', 'recorrente', 'recorrencia_valor', 'recorrencia_unidade']
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d' 
            ),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'recorrente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recorrencia_valor': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'recorrencia_unidade': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data'].initial = self.instance.data.strftime('%Y-%m-%d')
            self.fields['horario'].initial = self.instance.horario.strftime('%H:%M')