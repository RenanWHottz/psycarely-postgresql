#PsyCarely/core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')), 
    path('pacientes/', include('apps.pacientes.urls')),
    path('registros/', include('apps.registros.urls')),
    path('consultas/', include('apps.consultas.urls')),
]
