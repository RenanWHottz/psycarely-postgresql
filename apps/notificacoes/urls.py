#apps/notificacoes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('gerenciar/<int:paciente_id>/', views.gerenciar_notificacoes, name='gerenciar_notificacoes'),

    # CONSULTA
    path('consulta/<int:paciente_id>/<str:campo>/alternar/', 
         views.alternar_notificacao_consulta, 
         name='alternar_notificacao_consulta'),

    # HUMOR
    path('humor/<int:paciente_id>/criar/', 
         views.criar_notificacao_humor, 
         name='criar_notificacao_humor'),

    path('humor/<int:paciente_id>/<int:humor_id>/editar/', 
         views.editar_notificacao_humor, 
         name='editar_notificacao_humor'),

    path('humor/<int:paciente_id>/<int:humor_id>/excluir/', 
         views.excluir_notificacao_humor, 
         name='excluir_notificacao_humor'),

    # RPD
    path('rpd/<int:paciente_id>/criar/', 
         views.criar_notificacao_rpd, 
         name='criar_notificacao_rpd'),

    path('rpd/<int:paciente_id>/<int:rpd_id>/editar/', 
         views.editar_notificacao_rpd, 
         name='editar_notificacao_rpd'),

    path('rpd/<int:paciente_id>/<int:rpd_id>/excluir/', 
         views.excluir_notificacao_rpd, 
         name='excluir_notificacao_rpd'),
]
