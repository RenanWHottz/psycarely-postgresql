#apps/notificacoes/models.py
from django.db import models
from apps.usuarios.models import Usuario


class NotificacaoConsulta(models.Model):
    paciente = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificacao_consulta'
    )
    ativa_24h = models.BooleanField(default=True)
    ativa_2h = models.BooleanField(default=True)
    ativa_30min = models.BooleanField(default=True)

    def __str__(self):
        return f"Notificações de consulta - {self.paciente.get_full_name()}"


class NotificacaoHumor(models.Model):
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificacoes_humor'
    )
    horario = models.TimeField()

    def __str__(self):
        return f"{self.horario} - {self.paciente.get_full_name()}"


class NotificacaoRPD(models.Model):

    DIAS_SEMANA = [
        (0, "Domingo"),
        (1, "Segunda-feira"),
        (2, "Terça-feira"),
        (3, "Quarta-feira"),
        (4, "Quinta-feira"),
        (5, "Sexta-feira"),
        (6, "Sábado"),
    ]

    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificacoes_rpd'
    )
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    horario = models.TimeField()

    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.horario} ({self.paciente.get_full_name()})"
