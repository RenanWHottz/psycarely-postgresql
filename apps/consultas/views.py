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
from calendar import monthrange


@login_required
def listar_consultas(request, paciente_id):
    vinculo = get_object_or_404(Vinculo, paciente_id=paciente_id, profissional=request.user)
    consultas = Consulta.objects.filter(vinculo=vinculo).order_by('data', 'horario')
    recorrencia = Recorrencia.objects.filter(vinculo=vinculo).first()
    return render(request, 'consultas/listar_consultas.html', {
        'vinculo': vinculo,
        'consultas': consultas,
        'recorrencia': recorrencia
    })

@login_required
def excluir_recorrencia(request, recorrencia_id):
    recorrencia = get_object_or_404(Recorrencia, id=recorrencia_id, profissional=request.user)
    paciente_id = recorrencia.paciente.id
    recorrencia.delete()
    messages.success(request, "Recorrência e todas as consultas associadas foram excluídas.")
    return redirect('listar_consultas', paciente_id=paciente_id)

@login_required
def editar_recorrencia(request, recorrencia_id):
    recorrencia = get_object_or_404(Recorrencia, id=recorrencia_id, profissional=request.user)
    paciente_id = recorrencia.paciente.id

    if request.method == 'POST':
        valor = request.POST.get('recorrencia_valor')
        unidade = request.POST.get('recorrencia_unidade')
        horario = request.POST.get('horario_padrao')
        dia_semana = request.POST.get('dia_semana')

        if valor and unidade and horario is not None:
            recorrencia.recorrencia_valor = int(valor)
            recorrencia.recorrencia_unidade = unidade
            recorrencia.horario_padrao = horario
            recorrencia.dia_semana = int(dia_semana)
            recorrencia.save()

            Consulta.objects.filter(recorrencia=recorrencia).delete()
            data_inicial = timezone.localdate()

            while data_inicial.weekday() != recorrencia.dia_semana:
                data_inicial += timedelta(days=1)

            gerar_consultas_recorrentes(recorrencia, data_inicial)

            messages.success(request, "Recorrência e consultas recriadas com sucesso.")
            return redirect('listar_consultas', paciente_id=paciente_id)
        else:
            messages.error(request, "Preencha todos os campos corretamente.")
    
    return render(request, 'consultas/editar_recorrencia.html', {'recorrencia': recorrencia})

def gerar_consultas_recorrentes(recorrencia, data_inicial):
    data_final = data_inicial + relativedelta(months=6)
    data_atual = data_inicial

    while data_atual <= data_final:
        while data_atual.weekday() != recorrencia.dia_semana:
            data_atual += timedelta(days=1)

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
                gerar_consultas_recorrentes(recorrencia, consulta.data)
                return redirect('listar_consultas', paciente_id=paciente_id)
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
def calendario_consultas(request):
    from calendar import monthrange
    import calendar

    profissional = request.user
    hoje = date.today()

    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    primeiro_dia = date(ano, mes, 1)
    ultimo_dia = date(ano, mes, monthrange(ano, mes)[1])

    consultas = Consulta.objects.filter(
        profissional=profissional,
        data__range=[primeiro_dia, ultimo_dia]
    ).select_related('paciente').order_by('data', 'horario')

    consultas_por_dia = {}
    for consulta in consultas:
        dia = consulta.data.day
        consultas_por_dia.setdefault(dia, []).append(consulta)

    cal = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdayscalendar(ano, mes)

    meses = [
        (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), (4, "Abril"),
        (5, "Maio"), (6, "Junho"), (7, "Julho"), (8, "Agosto"),
        (9, "Setembro"), (10, "Outubro"), (11, "Novembro"), (12, "Dezembro")
    ]

    return render(request, 'consultas/calendario_consultas.html', {
        'semanas': semanas,
        'consultas_por_dia': consultas_por_dia,
        'mes': mes,
        'ano': ano,
        'meses': meses,
        'hoje': hoje,
    })

@login_required
def dashboard_paciente(request):
    """Exibe o dashboard do paciente com as 4 próximas consultas futuras."""
    hoje = timezone.localdate()

    proximas_consultas = (
        Consulta.objects.filter(
            paciente=request.user,
            data__gte=hoje  
        )
        .order_by('data', 'horario')[:4]  
    )

    return render(request, 'usuarios/dashboard_paciente.html', {
        'proximas_consultas': proximas_consultas
    })

@login_required
def calendario_paciente(request):
    import calendar
    hoje = date.today()

    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    primeiro_dia = date(ano, mes, 1)
    ultimo_dia = date(ano, mes, monthrange(ano, mes)[1])

    consultas = Consulta.objects.filter(
        paciente=request.user,
        data__range=[primeiro_dia, ultimo_dia]
    ).select_related('profissional').order_by('data', 'horario')

    consultas_por_dia = {}
    for consulta in consultas:
        dia = consulta.data.day
        consultas_por_dia.setdefault(dia, []).append(consulta)

    cal = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdayscalendar(ano, mes)

    meses = [
        (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), (4, "Abril"),
        (5, "Maio"), (6, "Junho"), (7, "Julho"), (8, "Agosto"),
        (9, "Setembro"), (10, "Outubro"), (11, "Novembro"), (12, "Dezembro")
    ]

    return render(request, 'consultas/calendario_paciente.html', {
        'semanas': semanas,
        'consultas_por_dia': consultas_por_dia,
        'mes': mes,
        'ano': ano,
        'meses': meses,
        'hoje': hoje,
    })
