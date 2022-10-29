from django.urls import path
#import django_cas_ng.views
from app.seguridad.presentation.views import views_autenticacion

urlpatterns = [
    path('cambiar-contrasena', views_autenticacion.cambiar_contrasena, name='cambiar_contrasena'),
    path('cerrar-sesion', views_autenticacion.cerrar_sesion, name='cerrar_sesion'),
    path('iniciar-sesion', views_autenticacion.iniciar_sesion, name='iniciar_sesion'),
    #path('iniciar-sesion/tipo_usuario', views_autenticacion.iniciar_sesion_tipo_usuario, name='iniciar_sesion_tipo_usuario'),
    #path('', views_autenticacion.iniciar_sesion, name='iniciar_sesion_base'),

    #autenticación cas
    #path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    #path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),

# Registro es relacionado al Inicio sesión

    #path('registro', views_autenticacion.registro_solicitante, name='registro_solicitante'),
    #path('registro/enviar_token', views_autenticacion.enviar_token, name='enviar_token'),
    #path('registro/verificar_token', views_autenticacion.verificar_token, name='verificar_token'),
    #path('registro/verificar_persona', views_autenticacion.verificar_persona, name='verificar_persona'),
    path('iniciar-sesion/solicitante', views_autenticacion.InicioSesionSolicitante.as_view(), name='inicio_sesion_solicitante'),
]
