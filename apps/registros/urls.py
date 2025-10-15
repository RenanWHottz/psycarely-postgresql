from django.urls import path
from . import views

urlpatterns = [
    path('tarefas/', views.tarefas_paciente, name='tarefas_paciente'),
    path('rpd/novo/', views.novo_rpd, name='novo_rpd'),
    path('rpd/listar/', views.listar_rpds, name='listar_rpds'),
    path('rpd/<int:rpd_id>/detalhar/', views.detalhar_rpd, name='detalhar_rpd'),
    path('rpd/<int:rpd_id>/editar/', views.editar_rpd, name='editar_rpd'),
    path('rpd/<int:rpd_id>/excluir/', views.excluir_rpd, name='excluir_rpd'),
]