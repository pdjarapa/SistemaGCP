from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404

#from app.core import DataTableParams
from app.seguridad.application.notificacion_app_service import NotificacionAppService
from app.seguridad.domain.models import Usuario
#from app.asistencia.infraestructure.external.siaaf_app_service import SiaafAppService

@login_required
def notificacion_usuario_detalle(request, id):
    """
    Muestra la notificacion al usuario
    :param request:
    :return:
    """
    notificacion_usuario = get_object_or_404(NotificacionUsuario, id=id)
    if notificacion_usuario.estado != NotificacionUsuario.ESTADO_LEIDO:
        notificacion_usuario.estado = NotificacionUsuario.ESTADO_LEIDO
        notificacion_usuario.save()
    return render(request, 'seguridad/notificacion/detalle.html', locals())


@login_required
def notificacion_usuario_lista(request):
    """
    Muestra todas las notificaciones del usuario
    :param request:
    :return:
    """
    import json
    notificacion_usuario_estados = json.dumps(dict(NotificacionUsuario.CHOICE_ESTADO))
    return render(request, 'seguridad/notificacion/lista.html', locals())


@login_required
def notificacion_usuario_lista_paginador(request):
    """
    Lista las asignaturas con la paginación de datatable
    :param request:
    :return:
    """
    try:

        notificacion_usuario_params = DataTableParams(request, **request.POST)
        NotificacionAppService.get_datatable(notificacion_usuario_params=notificacion_usuario_params)
        data = notificacion_usuario_params.items.values('id', 'notificacion__asunto', 'notificacion__created_at', 'estado').all()
        result = notificacion_usuario_params.result(list(data))
        return JsonResponse(result)

    except Exception as e:
        return HttpResponseServerError(e)


@login_required
def get_foto_thumbnail(request, user_id):
    user = Usuario.objects.get(id=user_id)
    data = SiaafAppService.get_foto_thumbnail(user.correo_electronico)
    if data:
        return JsonResponse(data, safe=False)
    return JsonResponse('', safe=False)