#apps/consultas/models.py:
from django.db import models
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.pacientes.models import Vinculo

class Consulta(models.Model):
    RECORRENCIA_UNIDADES = [
        ('semanas', 'Semanas'),
        ('meses', 'Meses'),
        ('anos', 'Anos'),
    ]

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

    recorrencia_valor = models.PositiveIntegerField(default=1)
    recorrencia_unidade = models.CharField(
        max_length=10,
        choices=RECORRENCIA_UNIDADES,
        default='semanas'
    )
    recorrente = models.BooleanField(default=False)

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.paciente.get_full_name()} em {self.data.strftime('%d/%m/%Y')} às {self.horario.strftime('%H:%M')}"

    class Meta:
        ordering = ['-data', '-horario']
