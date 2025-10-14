# apps/usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('dashboard/profissional/', views.dashboard_profissional, name='dashboard_profissional'),
    path('dashboard/paciente/', views.dashboard_paciente, name='dashboard_paciente'),
]