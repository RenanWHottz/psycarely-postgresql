# apps/usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, CadastroForm
from .decorators import profissional_required, paciente_required


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_profissional():
                return redirect('dashboard_profissional')
            else:
                return redirect('dashboard_paciente')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro_view(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
@profissional_required
def dashboard_profissional(request):
    #consultas, tarefas e notificações
    return render(request, 'usuarios/dashboard_profissional.html')

@login_required
@paciente_required
def dashboard_paciente(request):
    #consultas, RPD, registro de humor
    return render(request, 'usuarios/dashboard_paciente.html')