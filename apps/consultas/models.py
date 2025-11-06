#apps/consultas/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.usuarios.models import Usuario
from apps.pacientes.models import Vinculo


class Recorrencia(models.Model):

    RECORRENCIA_UNIDADES = [
        ('semanas', 'Semanas'),
        ('meses', 'Meses'),
        ('anos', 'Anos'),
    ]

    vinculo = models.OneToOneField(
        Vinculo,
        on_delete=models.CASCADE,
        related_name='recorrencia'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'profissional'},
        related_name='recorrencias_profissional'
    )
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='recorrencias_paciente'
    )

    recorrencia_valor = models.PositiveIntegerField(default=1)
    recorrencia_unidade = models.CharField(
        max_length=10,
        choices=RECORRENCIA_UNIDADES,
        default='semanas'
    )
    horario_padrao = models.TimeField()
    dia_semana = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Segunda-feira'),
            (1, 'Terça-feira'),
            (2, 'Quarta-feira'),
            (3, 'Quinta-feira'),
            (4, 'Sexta-feira'),
            (5, 'Sábado'),
            (6, 'Domingo'),
        ],
        help_text="Dia da semana da consulta recorrente"
    )
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"Recorrência de {self.paciente.get_full_name()} ({self.get_recorrencia_unidade_display()})"


class Consulta(models.Model):
    vinculo = models.ForeignKey(
        Vinculo,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'profissional'},
        related_name='consultas_profissional'
    )
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='consultas_paciente'
    )

    data = models.DateField()
    horario = models.TimeField()
    recorrencia = models.ForeignKey(
        Recorrencia,
        on_delete=models.CASCADE,  
        null=True, blank=True,
        related_name='consultas_geradas'
    )

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.paciente.get_full_name()} em {self.data.strftime('%d/%m/%Y')} às {self.horario.strftime('%H:%M')}"

    class Meta:
        ordering = ['-data', '-horario']
        unique_together = ('profissional', 'data', 'horario')
