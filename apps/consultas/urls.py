#apps/consultas/urls.py:
from django.urls import path
from . import views

urlpatterns = [
    path('<int:paciente_id>/', views.listar_consultas, name='listar_consultas'),
    path('<int:paciente_id>/marcar/', views.marcar_consulta, name='marcar_consulta'),
    path('editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('recorrencia/<int:recorrencia_id>/editar/', views.editar_recorrencia, name='editar_recorrencia'),
    path('recorrencia/<int:recorrencia_id>/excluir/', views.excluir_recorrencia, name='excluir_recorrencia'),
    path('dashboard/', views.dashboard_profissional, name='dashboard_profissional'),
    path('calendario/', views.calendario_consultas, name='calendario_consultas'),
    path('dashboard_paciente/', views.dashboard_paciente, name='dashboard_paciente'),
    path('calendario_paciente/', views.calendario_paciente, name='calendario_paciente'),
]
