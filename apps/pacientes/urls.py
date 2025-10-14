#apps/pacientes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pacientes, name='lista_pacientes'),
    path('<int:paciente_id>/', views.perfil_paciente, name='perfil_paciente'),
    path('enviar-solicitacao/', views.enviar_solicitacao, name='enviar_solicitacao'),
    path('solicitacoes/', views.lista_solicitacoes, name='lista_solicitacoes'),
    path('solicitacoes/<int:solicitacao_id>/aprovar/', views.aprovar_solicitacao, name='aprovar_solicitacao'),
    path('solicitacoes/<int:solicitacao_id>/excluir/', views.excluir_solicitacao, name='excluir_solicitacao'),
    path('desconectar/', views.desconectar_profissional, name='desconectar_profissional'),
]
