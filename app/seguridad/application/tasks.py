# Create your tasks her
from __future__ import absolute_import, unicode_literals

from datetime import datetime

from celery import shared_task

from app.core import enviar_correo
from app.seguridad.application.notificacion_app_service import NotificacionAppService
from app.seguridad.domain.models import Notificacion, NotificacionUsuario


@shared_task
def notificaciones_enviar_correo():
    """
    tarea para enviar los correos de las notificaciones pendientes
    :return:
    """
    notificaciones = Notificacion.objects.filter(
        envio_email=None, notificacionusuario__estado=NotificacionUsuario.ESTADO_PENDIENTE).distinct().all()

    for notificacion in notificaciones:
        destinatarios = NotificacionUsuario.objects.filter(notificacion=notificacion,
            estado=NotificacionUsuario.ESTADO_PENDIENTE).values_list('usuario__correo_electronico', flat=True).all()
        if destinatarios:
            texto = NotificacionAppService.html_email(notificacion)
            enviar_correo(notificacion.asunto, texto, destinatarios)
        notificacion.envio_email = datetime.now()
        notificacion.save()
