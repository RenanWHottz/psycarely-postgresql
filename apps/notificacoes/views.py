#apps/notificacoes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .models import NotificacaoConsulta, NotificacaoHumor, NotificacaoRPD
from apps.usuarios.models import Usuario
from datetime import datetime


def gerenciar_notificacoes(request, paciente_id):
    paciente = get_object_or_404(Usuario, id=paciente_id, tipo='paciente')

    consulta_notificacao, created = NotificacaoConsulta.objects.get_or_create(
        paciente=paciente
    )

    humor = paciente.notificacoes_humor.all()
    rpd = paciente.notificacoes_rpd.all()

    contexto = {
        "paciente": paciente,
        "notificacoes_consulta": consulta_notificacao,
        "notificacoes_humor": humor,
        "notificacoes_rpd": rpd,
        "NotificacaoRPD": NotificacaoRPD,
        "dias_semana": NotificacaoRPD.DIAS_SEMANA,
    }

    return render(request, "notificacoes/gerenciar_notificacoes.html", contexto)


# ---------- CONSULTA ----------
def alternar_notificacao_consulta(request, paciente_id, campo):
    if campo not in ["ativa_24h", "ativa_2h", "ativa_30min"]:
        return HttpResponseBadRequest("Campo inválido")

    paciente = get_object_or_404(Usuario, id=paciente_id, tipo="paciente")
    consulta, created = NotificacaoConsulta.objects.get_or_create(paciente=paciente)

    valor_atual = getattr(consulta, campo)
    setattr(consulta, campo, not valor_atual)
    consulta.save()

    return redirect("gerenciar_notificacoes", paciente_id=paciente.id)


# ---------- HUMOR ----------
def criar_notificacao_humor(request, paciente_id):
    paciente = get_object_or_404(Usuario, id=paciente_id, tipo="paciente")

    horario = request.POST.get("horario")
    if not horario:
        return HttpResponseBadRequest("Horário inválido")

    if paciente.notificacoes_humor.count() >= 2:
        return HttpResponseBadRequest("Limite de 2 horários atingido")

    # Conversão correta para TimeField
    hora_formatada = datetime.strptime(horario, "%H:%M").time()

    NotificacaoHumor.objects.create(
        paciente=paciente,
        horario=hora_formatada
    )

    return redirect("gerenciar_notificacoes", paciente_id=paciente.id)


def editar_notificacao_humor(request, paciente_id, humor_id):
    notif = get_object_or_404(NotificacaoHumor, id=humor_id)
    horario = request.POST.get("horario")

    if not horario:
        return HttpResponseBadRequest("Horário inválido")

    notif.horario = datetime.strptime(horario, "%H:%M").time()
    notif.save()

    return redirect("gerenciar_notificacoes", paciente_id=notif.paciente.id)


def excluir_notificacao_humor(request, paciente_id, humor_id):
    notif = get_object_or_404(NotificacaoHumor, id=humor_id)
    paciente_id = notif.paciente.id
    notif.delete()

    return redirect("gerenciar_notificacoes", paciente_id=paciente_id)


# ---------- RPD ----------
def criar_notificacao_rpd(request, paciente_id):
    paciente = get_object_or_404(Usuario, id=paciente_id, tipo="paciente")

    dia = request.POST.get("dia")
    horario = request.POST.get("horario")

    if not dia or not horario:
        return HttpResponseBadRequest("Dados inválidos")

    if paciente.notificacoes_rpd.count() >= 2:
        return HttpResponseBadRequest("Limite semanal atingido")

    hora_formatada = datetime.strptime(horario, "%H:%M").time()

    NotificacaoRPD.objects.create(
        paciente=paciente,
        dia_semana=dia,
        horario=hora_formatada
    )

    return redirect("gerenciar_notificacoes", paciente_id=paciente.id)


def editar_notificacao_rpd(request, paciente_id, rpd_id):
    notif = get_object_or_404(NotificacaoRPD, id=rpd_id)

    dia = request.POST.get("dia")
    horario = request.POST.get("horario")

    if not dia or not horario:
        return HttpResponseBadRequest("Dados inválidos")

    notif.dia_semana = dia
    notif.horario = datetime.strptime(horario, "%H:%M").time()
    notif.save()

    return redirect("gerenciar_notificacoes", paciente_id=notif.paciente.id)


def excluir_notificacao_rpd(request, paciente_id, rpd_id):
    notif = get_object_or_404(NotificacaoRPD, id=rpd_id)
    paciente_id = notif.paciente.id
    notif.delete()

    return redirect("gerenciar_notificacoes", paciente_id=paciente_id)
