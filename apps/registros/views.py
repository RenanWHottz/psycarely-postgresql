#apps/registros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RPD
from .forms import RPDForm

@login_required
def tarefas_paciente(request):
    return render(request, 'registros/tarefas_paciente.html')

@login_required
def novo_rpd(request):
    if request.method == 'POST':
        form = RPDForm(request.POST)
        if form.is_valid():
            rpd = form.save(commit=False)
            rpd.paciente = request.user
            if hasattr(request.user, 'vinculo') and request.user.vinculo.ativo:
                rpd.profissional = request.user.vinculo.profissional
            rpd.save()
            return redirect('listar_rpds')
    else:
        form = RPDForm()
    return render(request, 'registros/novo_rpd.html', {'form': form})

@login_required
def listar_rpds(request):
    rpds = RPD.objects.filter(paciente=request.user).order_by('-data_criacao')
    return render(request, 'registros/listar_rpds.html', {'rpds': rpds})

@login_required
def detalhar_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    return render(request, 'registros/detalhar_rpd.html', {'rpd': rpd})

@login_required
def editar_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    if request.method == 'POST':
        form = RPDForm(request.POST, instance=rpd)
        if form.is_valid():
            form.save()
            return redirect('listar_rpds')
    else:
        form = RPDForm(instance=rpd)
    return render(request, 'registros/editar_rpd.html', {'form': form})

@login_required
def excluir_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    if request.method == 'POST':
        rpd.delete()
        return redirect('listar_rpds')
    return render(request, 'registros/listar_rpds.html', {'rpd': rpd})