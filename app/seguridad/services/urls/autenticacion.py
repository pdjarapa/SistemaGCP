from django.urls import path
from app.seguridad.presentation.views import views_autenticacion

urlpatterns = [
    path('cambiar-contrasena', views_autenticacion.cambiar_contrasena, name='cambiar_contrasena'),
    path('cerrar-sesion', views_autenticacion.cerrar_sesion, name='cerrar_sesion'),
    path('iniciar-sesion', views_autenticacion.iniciar_sesion, name='iniciar_sesion'),
]
