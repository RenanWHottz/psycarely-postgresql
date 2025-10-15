#apps/registros/models.py
from django.db import models
from apps.usuarios.models import Usuario

class RPD(models.Model):
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='rpds'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        limit_choices_to={'tipo': 'profissional'},
        null=True,
        blank=True,
        related_name='rpds_pacientes'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_acontecimento = models.DateTimeField(null=True, blank=True)

    situacao = models.TextField()
    pensamentos_automaticos = models.TextField()
    emocao = models.TextField()
    conclusao = models.TextField()
    resultado = models.TextField()

    def __str__(self):
        return f"RPD de {self.paciente.get_full_name()} ({self.data_criacao.strftime('%d/%m/%Y')})"
