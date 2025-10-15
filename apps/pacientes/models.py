# apps/pacientes/models.py
from django.db import models
from apps.usuarios.models import Usuario

class Vinculo(models.Model):
    paciente = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='vinculo'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'profissional'},
        related_name='vinculos'
    )
    ativo = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profissional.get_full_name()} ↔ {self.paciente.get_full_name()} (ativo={self.ativo})"


class SolicitacaoConexao(models.Model):
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='solicitacoes_recebidas'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'profissional'},
        related_name='solicitacoes_enviadas'
    )
    aprovado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('paciente', 'profissional')

    def __str__(self):
        return f"{self.profissional} → {self.paciente} ({'Aprovado' if self.aprovado else 'Pendente'})"

class Anamnese(models.Model):
    vinculo = models.OneToOneField(
        'Vinculo',
        on_delete=models.CASCADE,
        related_name='anamnese'
    )
    conteudo = models.TextField(blank=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Anamnese de {self.vinculo.paciente.get_full_name()} ({self.vinculo.profissional.get_full_name()})"
