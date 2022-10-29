from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Pagina principal del usuario cuando esta loqueado
    :param request:
    :return:
    """
    usuario = request.user
    autenticado = request.user.is_authenticated

    if autenticado:
        #from app.asistencia.application.grupo_app_service import GrupoAppService
        #from app.seguridad.application.usuario_app_service import UsuarioAppService

        #UsuarioAppService.inicializar_usuario(usuario)
        #miembros = GrupoAppService.get_miembros_registro_asistencia(usuario)
        return render(request, 'seguridad/usuario/detalle.html', locals())
    else:
        #lista_tramite = TramiteAppService.get_todos_activo()
        return render(request, 'home.html', locals())