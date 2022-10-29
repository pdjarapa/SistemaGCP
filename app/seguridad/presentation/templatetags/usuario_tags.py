from django import template
from django.conf import settings
from django.urls import reverse

#from app.seguridad.application import UsuarioAppService
#from app.seguridad.domain.models import Funcionalidad
#from app.tramite.layer.application.proceso_app_service import ProcesoAppService
#from app.tramite.layer.security.proceso_sec_service import ProcesoSecService

register = template.Library()

@register.simple_tag
def get_funcionalidades(usuario):
    return UsuarioAppService.get_funcionalidades(usuario, Funcionalidad.MODULO_SIAAF)

@register.simple_tag
def get_nro_notificaciones(usuario):
    return UsuarioAppService.get_nro_notificaciones(usuario)

@register.simple_tag
def get_ultimas_notificaciones(usuario):
    return UsuarioAppService.get_ultimas_notificaciones(usuario)

@register.simple_tag
def get_logout_action(request):
    is_cas_authenticated = request.session.get('is_cas_authenticated', False)
    logout = reverse('seguridad:cas_ng_logout') + ('?next=/%s' % settings.BASEHREF) if is_cas_authenticated else reverse('seguridad:cerrar_sesion')
    return logout


@register.simple_tag
def get_password_action(request):
    is_cas_authenticated = request.session.get('is_cas_authenticated', False)
    url_action =  '%s/perfilUsuario.php' % settings.SAC_URL if is_cas_authenticated else reverse('seguridad:cambiar_contrasena')
    return url_action

@register.simple_tag
def get_es_actor(usuario):
    #return ProcesoSecService.get_es_actor(usuario)
    return False