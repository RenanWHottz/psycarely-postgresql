#apps/registros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.usuarios.decorators import profissional_required, paciente_required
from django.contrib.auth.decorators import login_required
from .models import RPD
from .forms import RPDForm

@login_required
@paciente_required
def tarefas_paciente(request):
    return render(request, 'registros/tarefas_paciente.html')

@login_required
@paciente_required
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
@paciente_required
def listar_rpds(request):
    rpds = RPD.objects.filter(paciente=request.user).order_by('-data_criacao')
    return render(request, 'registros/listar_rpds.html', {'rpds': rpds})

@login_required
@paciente_required
def detalhar_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    return render(request, 'registros/detalhar_rpd.html', {'rpd': rpd})

@login_required
@paciente_required
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
@paciente_required
def excluir_rpd(request, rpd_id):
    rpd = get_object_or_404(RPD, id=rpd_id, paciente=request.user)
    if request.method == 'POST':
        rpd.delete()
        return redirect('listar_rpds')
    return render(request, 'registros/listar_rpds.html', {'rpd': rpd})

@login_required
@profissional_required
def listar_rpds_paciente(request, paciente_id):
    from apps.pacientes.models import Vinculo
    vinculo = get_object_or_404(Vinculo, paciente__id=paciente_id, profissional=request.user, ativo=True)
    paciente = vinculo.paciente

    rpds = RPD.objects.filter(paciente=paciente).order_by('-data_criacao')

    context = {
        'rpds': rpds,
        'paciente': paciente,
    }
    return render(request, 'registros/listar_rpds_profissional.html', context)

@login_required
@profissional_required
def detalhar_rpd_profissional(request, rpd_id):
    from apps.pacientes.models import Vinculo
    if not Vinculo.objects.filter(paciente=rpd.paciente, profissional=request.user, ativo=True).exists():
        return redirect('lista_pacientes')

    return render(request, 'registros/detalhar_rpd_profissional.html', {'rpd': rpd})