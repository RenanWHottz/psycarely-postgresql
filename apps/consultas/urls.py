#apps/consultas/urls.py:
from django.urls import path
from . import views

urlpatterns = [
    path('<int:paciente_id>/', views.listar_consultas, name='listar_consultas'),
    path('<int:paciente_id>/marcar/', views.marcar_consulta, name='marcar_consulta'),
    path('editar/<int:consulta_id>/', views.editar_consulta, name='editar_consulta'),
    path('dashboard/', views.dashboard_profissional, name='dashboard_profissional'),
    path('calendario/', views.calendario_consultas, name='calendario_consultas'),
    path('events/', views.calendar_events, name='calendar_events'),
]
