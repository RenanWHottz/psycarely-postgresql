#apps/registros/models.py
from django.db import models
from django.utils import timezone
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

class RegistroHumor(models.Model):
    EMOCOES_CHOICES = [
        ('feliz', '😄 Feliz'),
        ('triste', '😢 Triste'),
        ('ansioso', '😰 Ansioso(a)'),
        ('tranquilo', '😌 Tranquilo(a)'),
        ('irritado', '😠 Irritado(a)'),
        ('desanimado', '😞 Desanimado(a)'),
        ('esperancoso', '😊 Esperançoso(a)'),
    ]

    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='registros_humor'
    )
    data_humor = models.DateTimeField(default=timezone.now)
    emocao = models.CharField(max_length=20, choices=EMOCOES_CHOICES)

    def __str__(self):
        return f"{self.paciente.get_full_name()} - {self.get_emocao_display()} ({self.data_humor.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        ordering = ['-data_humor']

class AnotacaoGeral(models.Model):
    paciente = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='anotacao_geral'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        limit_choices_to={'tipo': 'profissional'},
        null=True,
        blank=True,
        related_name='anotacoes_gerais'
    )
    conteudo = models.TextField(blank=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Anotação Geral - {self.paciente.get_full_name()}"

class AnotacaoConsulta(models.Model):
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'paciente'},
        related_name='anotacoes_consulta_paciente'
    )
    profissional = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        limit_choices_to={'tipo': 'profissional'},
        null=True,
        blank=True,
        related_name='anotacoes_consulta_profissional'
    )
    data_consulta = models.DateField(default=timezone.now)
    conteudo = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Anotação de Consulta - {self.paciente.get_full_name()} ({self.data_consulta.strftime('%d/%m/%Y')})"

    class Meta:
        ordering = ['-data_consulta']
