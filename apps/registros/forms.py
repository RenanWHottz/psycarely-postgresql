#apps/registros/forms.py
from django import forms
from django.utils import timezone
from .models import RPD, RegistroHumor

class RPDForm(forms.ModelForm):
    class Meta:
        model = RPD
        fields = [
            'data_acontecimento',
            'situacao',
            'pensamentos_automaticos',
            'emocao',
            'conclusao',
            'resultado'
        ]
        widgets = {
            'data_acontecimento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'situacao': forms.Textarea(attrs={'rows': 2}),
            'pensamentos_automaticos': forms.Textarea(attrs={'rows': 2}),
            'emocao': forms.Textarea(attrs={'rows': 2}),
            'conclusao': forms.Textarea(attrs={'rows': 2}),
            'resultado': forms.Textarea(attrs={'rows': 2}),
        }

class RegistroHumorForm(forms.ModelForm):
    class Meta:
        model = RegistroHumor
        fields = ['data_humor', 'emocao']
        widgets = {
            'data_humor': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        agora = timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M")
        # Define valor inicial se não vier do POST
        if not self.data.get('data_humor'):
            self.initial['data_humor'] = agora
            # aplica também no widget (garante exibição no input)
            self.fields['data_humor'].widget.attrs['value'] = agora

    def clean_data_humor(self):
        data = self.cleaned_data['data_humor']
        if data > timezone.now():
            raise forms.ValidationError("A data e hora devem ser anteriores ao momento atual.")
        return data