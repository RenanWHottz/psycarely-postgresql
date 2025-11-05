#apps/consultas/views.py:
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from apps.pacientes.models import Vinculo
from .models import Consulta, Recorrencia
from .forms import ConsultaForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


@login_required
def listar_consultas(request, paciente_id):
    vinculo = get_object_or_404(Vinculo, paciente_id=paciente_id, profissional=request.user)
    consultas = Consulta.objects.filter(vinculo=vinculo).order_by('data', 'horario')
    return render(request, 'consultas/listar_consultas.html', {'vinculo': vinculo, 'consultas': consultas})


def gerar_consultas_recorrentes(recorrencia, data_inicial):
    """
    Gera automaticamente consultas para os próximos 6 meses a partir da data inicial.
    """
    data_final = data_inicial + relativedelta(months=6)
    data_atual = data_inicial

    while data_atual <= data_final:
        # Avança até o próximo dia da semana configurado
        while data_atual.weekday() != recorrencia.dia_semana:
            data_atual += timedelta(days=1)

        # Cria consulta se ainda não existir
        if not Consulta.objects.filter(
            profissional=recorrencia.profissional,
            data=data_atual,
            horario=recorrencia.horario_padrao
        ).exists():
            Consulta.objects.create(
                vinculo=recorrencia.vinculo,
                profissional=recorrencia.profissional,
                paciente=recorrencia.paciente,
                data=data_atual,
                horario=recorrencia.horario_padrao,
                recorrencia=recorrencia
            )

        # Avança conforme a unidade e valor da recorrência
        if recorrencia.recorrencia_unidade == 'semanas':
            data_atual += timedelta(weeks=recorrencia.recorrencia_valor)
        elif recorrencia.recorrencia_unidade == 'meses':
            data_atual += relativedelta(months=recorrencia.recorrencia_valor)
        elif recorrencia.recorrencia_unidade == 'anos':
            data_atual += relativedelta(years=recorrencia.recorrencia_valor)
        else:
            break


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

                # 🔥 Gera automaticamente as consultas futuras
                gerar_consultas_recorrentes(recorrencia, consulta.data)
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


@login_required
def dashboard_profissional(request):
    """Exibe o dashboard do profissional com as próximas 4 consultas (a partir de hoje)."""
    hoje = timezone.localdate()
    proximas = Consulta.objects.filter(
        profissional=request.user,
        data__gte=hoje
    ).order_by('data', 'horario')[:4]

    return render(request, 'usuarios/dashboard_profissional.html', {'proximas_consultas': proximas})


@login_required
def calendar_events(request):
    """
    Endpoint JSON para o FullCalendar.
    Recebe GET params 'start' e 'end' no formato ISO e retorna eventos no intervalo.
    """
    start = request.GET.get('start')
    end = request.GET.get('end')
    try:
        start_date = datetime.fromisoformat(start).date() if start else timezone.localdate()
        end_date = datetime.fromisoformat(end).date() if end else start_date + timedelta(days=30)
    except Exception:
        start_date = timezone.localdate()
        end_date = start_date + timedelta(days=30)

    eventos = Consulta.objects.filter(
        profissional=request.user,
        data__gte=start_date,
        data__lte=end_date
    ).order_by('data', 'horario')

    items = []
    for c in eventos:
        start_dt = datetime.combine(c.data, c.horario)
        end_dt = start_dt + timedelta(hours=1)
        items.append({
            'id': c.id,
            'title': f"{c.paciente.get_full_name()}",
            'start': start_dt.isoformat(),
            'end': end_dt.isoformat(),
            'allDay': False,
            'recorrencia_id': c.recorrencia.id if c.recorrencia else None,
        })

    return JsonResponse(items, safe=False)


@login_required
def calendario_consultas(request):
    """Renderiza a página do calendário do profissional."""
    return render(request, 'consultas/calendario_consultas.html')
