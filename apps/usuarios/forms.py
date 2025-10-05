# apps/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário ou CPF")
    password = forms.CharField(widget=forms.PasswordInput)

class CadastroForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=30, required=True)
    last_name = forms.CharField(label="Sobrenome", max_length=150, required=True)
    tipo = forms.ChoiceField(
        choices=[('profissional', 'Profissional'), ('paciente', 'Paciente')],
        widget=forms.RadioSelect,
        label="Tipo de usuário"
    )
    cpf = forms.CharField(label="CPF", required=True)
    crp = forms.CharField(label="CRP", required=False)
    email = forms.EmailField(label="E-mail")
    telefone = forms.CharField(label="Telefone", required=False)

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'tipo', 'cpf', 'crp', 
            'email', 'telefone', 'password1', 'password2'
        ]
        labels = {
            'username': 'Usuário',
            'password1': 'Senha',
            'password2': 'Confirme a senha'
        }
        help_texts = {
            'username': None,
            'password1': "Sua senha deve ter pelo menos 8 caracteres.",
            'password2': "Digite a mesma senha para confirmação."
        }
