# apps/consultas/admin.py
from django.contrib import admin
from .models import Consulta

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'paciente', 'profissional', 'data', 'horario', 
        'recorrente_display', 'recorrencia_valor_display', 'recorrencia_unidade_display'
    )

    list_filter = ('data', 'recorrencia__recorrencia_unidade', 'recorrencia__ativa')

    def recorrente_display(self, obj):
        return obj.recorrencia is not None
    recorrente_display.boolean = True
    recorrente_display.short_description = 'Recorrente'

    def recorrencia_valor_display(self, obj):
        if obj.recorrencia:
            return obj.recorrencia.recorrencia_valor
        return None
    recorrencia_valor_display.short_description = 'Valor Recorrência'

    def recorrencia_unidade_display(self, obj):
        if obj.recorrencia:
            return obj.recorrencia.recorrencia_unidade
        return None
    recorrencia_unidade_display.short_description = 'Unidade Recorrência'
