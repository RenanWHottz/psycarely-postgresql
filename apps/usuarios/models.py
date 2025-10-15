from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    tipo = models.CharField(
        max_length=20,
        choices=[('profissional', 'Profissional'), ('paciente', 'Paciente')]
    )
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    crp = models.CharField(max_length=7, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255, blank=True)

    def is_profissional(self):
        return self.tipo == 'profissional'

    def is_paciente(self):
        return self.tipo == 'paciente'

    def save(self, *args, **kwargs):
        # Limita CRP apenas para profissionais
        if not self.is_profissional():
            self.crp = None
        super().save(*args, **kwargs)
