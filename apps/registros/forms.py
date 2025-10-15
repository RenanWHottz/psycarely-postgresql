#apps/registros/forms.py
from django import forms
from .models import RPD

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
