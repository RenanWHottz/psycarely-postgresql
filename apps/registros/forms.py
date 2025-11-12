#apps/registros/forms.py
from django import forms
from django.utils import timezone
from .models import RPD, RegistroHumor, AnotacaoGeral, AnotacaoConsulta

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
        if not self.data.get('data_humor'):
            self.initial['data_humor'] = agora
            self.fields['data_humor'].widget.attrs['value'] = agora

    def clean_data_humor(self):
        data = self.cleaned_data['data_humor']
        if data > timezone.now():
            raise forms.ValidationError("A data e hora devem ser anteriores ao momento atual.")
        return data

class AnotacaoGeralForm(forms.ModelForm):
    class Meta:
        model = AnotacaoGeral
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'rows': 12,
                'class': 'form-control',
                'placeholder': 'Escreva suas anotações sobre este paciente aqui...',
            })
        }

class AnotacaoConsultaForm(forms.ModelForm):
    class Meta:
        model = AnotacaoConsulta
        fields = ['data_consulta', 'conteudo']
        widgets = {
            'data_consulta': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'conteudo': forms.Textarea(attrs={
                'rows': 10,
                'class': 'form-control',
                'placeholder': 'Escreva as observações da consulta aqui...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('data_consulta') and not self.initial.get('data_consulta'):
            hoje = timezone.localdate().strftime("%Y-%m-%d")
            self.initial['data_consulta'] = hoje
            self.fields['data_consulta'].widget.attrs['value'] = hoje

    def clean_data_consulta(self):
        data = self.cleaned_data['data_consulta']
        if data > timezone.localdate():
            raise forms.ValidationError("A data da consulta não pode ser futura.")
        return data
