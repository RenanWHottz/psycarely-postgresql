# apps/consultas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from apps.pacientes.models import Vinculo
from .models import Consulta, Recorrencia
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

            # Lógica de recorrência
            if form.cleaned_data.get('recorrente'):
                recorrencia, created = Recorrencia.objects.get_or_create(
                    vinculo=vinculo,
                    profissional=consulta.profissional,
                    paciente=consulta.paciente,
                    defaults={
                        'recorrencia_valor': form.cleaned_data['recorrencia_valor'],
                        'recorrencia_unidade': form.cleaned_data['recorrencia_unidade'],
                        'horario_padrao': consulta.horario,
                        'dia_semana': consulta.data.weekday()
                    }
                )
                if not created:
                    recorrencia.recorrencia_valor = form.cleaned_data['recorrencia_valor']
                    recorrencia.recorrencia_unidade = form.cleaned_data['recorrencia_unidade']
                    recorrencia.horario_padrao = consulta.horario
                    recorrencia.dia_semana = consulta.data.weekday()
                    recorrencia.save()
                consulta.recorrencia = recorrencia
            else:
                consulta.recorrencia = None

            try:
                consulta.save()
                messages.success(request, "Consulta marcada com sucesso!")
            except IntegrityError:
                messages.error(request, "Já existe uma consulta marcada para este horário.")
                return render(request, 'consultas/marcar_consulta.html', {'form': form, 'vinculo': vinculo})

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
            messages.success(request, "Consulta excluída com sucesso.")
            return redirect('listar_consultas', paciente_id=paciente_id)

        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            # Atualiza recorrência
            if form.cleaned_data.get('recorrente'):
                recorrencia, created = Recorrencia.objects.get_or_create(
                    vinculo=consulta.vinculo,
                    profissional=consulta.profissional,
                    paciente=consulta.paciente,
                    defaults={
                        'recorrencia_valor': form.cleaned_data['recorrencia_valor'],
                        'recorrencia_unidade': form.cleaned_data['recorrencia_unidade'],
                        'horario_padrao': consulta.horario
                    }
                )
                if not created:
                    recorrencia.recorrencia_valor = form.cleaned_data['recorrencia_valor']
                    recorrencia.recorrencia_unidade = form.cleaned_data['recorrencia_unidade']
                    recorrencia.horario_padrao = consulta.horario
                    recorrencia.save()
                consulta.recorrencia = recorrencia
            else:
                consulta.recorrencia = None

            try:
                form.save()
                messages.success(request, "Consulta atualizada com sucesso.")
            except IntegrityError:
                messages.error(request, "Já existe uma consulta marcada para este horário.")

            return redirect('listar_consultas', paciente_id=consulta.paciente.id)
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'consultas/editar_consulta.html', {'form': form, 'consulta': consulta})
