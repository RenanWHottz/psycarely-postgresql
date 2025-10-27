#apps/consultas/views.py:
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.pacientes.models import Vinculo
from .models import Consulta
from .forms import ConsultaForm

@login_required
def listar_consultas(request, paciente_id):
    vinculo = get_object_or_404(Vinculo, paciente_id=paciente_id, profissional=request.user)
    consultas = Consulta.objects.filter(vinculo=vinculo).order_by('data', 'horario')
    return render(request, 'consultas/listar_consultas.html', {'vinculo': vinculo, 'consultas': consultas})

@login_required
def marcar_consulta(request, paciente_id):
    vinculo = get_object_or_404(Vinculo, paciente_id=paciente_id, profissional=request.user)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.vinculo = vinculo
            consulta.profissional = vinculo.profissional
            consulta.paciente = vinculo.paciente
            consulta.save()
            return redirect('listar_consultas', paciente_id=paciente_id)
    else:
        form = ConsultaForm()
    return render(request, 'consultas/marcar_consulta.html', {'form': form, 'vinculo': vinculo})

@login_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id, profissional=request.user)
    if request.method == 'POST':
        if 'excluir' in request.POST:
            paciente_id = consulta.paciente.id
            consulta.delete()
            return redirect('listar_consultas', paciente_id=paciente_id)

        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('listar_consultas', paciente_id=consulta.paciente.id)
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'consultas/editar_consulta.html', {'form': form, 'consulta': consulta})
