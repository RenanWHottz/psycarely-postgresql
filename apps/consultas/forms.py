#apps/consultas/forms.py:
from django import forms
from .models import Consulta, Recorrencia

class ConsultaForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        )
    )

    horario = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control'},
            format='%H:%M'
        )
    )

    recorrente = forms.BooleanField(required=False, label="Consulta recorrente")
    recorrencia_valor = forms.IntegerField(min_value=1, initial=1, required=False)
    recorrencia_unidade = forms.ChoiceField(
        choices=Recorrencia.RECORRENCIA_UNIDADES,
        required=False
    )

    class Meta:
        model = Consulta
        fields = ['data', 'horario', 'recorrente', 'recorrencia_valor', 'recorrencia_unidade']
        widgets = {
            'recorrente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recorrencia_valor': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'recorrencia_unidade': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and not self.data:
            self.fields['data'].initial = self.instance.data.strftime('%Y-%m-%d')
            self.fields['horario'].initial = self.instance.horario.strftime('%H:%M')
            if self.instance.recorrencia:
                self.fields['recorrente'].initial = True
                self.fields['recorrencia_valor'].initial = self.instance.recorrencia.recorrencia_valor
                self.fields['recorrencia_unidade'].initial = self.instance.recorrencia.recorrencia_unidade
