#apps/usuarios/decorators.py
from django.shortcuts import redirect
from django.contrib import messages

def profissional_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_profissional():
            messages.error(request, "Acesso restrito a profissionais.")
            return redirect('dashboard_paciente')
        return view_func(request, *args, **kwargs)
    return wrapper

def paciente_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_paciente():
            messages.error(request, "Acesso restrito a pacientes.")
            return redirect('dashboard_profissional')
        return view_func(request, *args, **kwargs)
    return wrapper
