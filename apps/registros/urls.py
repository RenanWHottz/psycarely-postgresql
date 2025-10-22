#apps/registros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tarefas/', views.tarefas_paciente, name='tarefas_paciente'),
    path('rpd/novo/', views.novo_rpd, name='novo_rpd'),
    path('rpd/listar/', views.listar_rpds, name='listar_rpds'),
    path('rpd/<int:rpd_id>/detalhar/', views.detalhar_rpd, name='detalhar_rpd'),
    path('rpd/<int:rpd_id>/editar/', views.editar_rpd, name='editar_rpd'),
    path('rpd/<int:rpd_id>/excluir/', views.excluir_rpd, name='excluir_rpd'),
    path('profissional/paciente/<int:paciente_id>/rpds/', views.listar_rpds_paciente, name='listar_rpds_paciente'),
    path('profissional/rpd/<int:rpd_id>/', views.detalhar_rpd_profissional, name='detalhar_rpd_profissional'),
    path('humor/novo/', views.registrar_humor, name='registrar_humor'),
    path('humor/listar/', views.listar_humores, name='listar_humores'),
    path('profissional/paciente/<int:paciente_id>/humores/', views.listar_humores_paciente, name='listar_humores_paciente'),
    path('profissional/paciente/<int:paciente_id>/anotacao-geral/', views.editar_anotacao_geral, name='editar_anotacao_geral'),
    path('profissional/paciente/<int:paciente_id>/anotacoes/', views.listar_anotacoes_paciente, name='listar_anotacoes_paciente'),
    path('profissional/paciente/<int:paciente_id>/anotacao-consulta/nova/', views.nova_anotacao_consulta, name='nova_anotacao_consulta'),
    path('profissional/anotacao-consulta/<int:anotacao_id>/editar/', views.editar_anotacao_consulta, name='editar_anotacao_consulta'),
]