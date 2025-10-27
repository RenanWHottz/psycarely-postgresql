#apps/consultas/admin.py:
from django.contrib import admin
from .models import Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'profissional', 'data', 'horario', 'recorrente')
    list_filter = ('profissional', 'recorrente', 'recorrencia_unidade')
    search_fields = ('paciente__first_name', 'profissional__first_name')
