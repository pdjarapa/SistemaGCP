from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string

from app.seguridad.domain.models import Notificacion, NotificacionUsuario


class NotificacionAppService(object):

    @staticmethod
    def crear_notificacion(asunto, mensaje, url, usuarios):
        """
        Creación de notificaciones a usuarios
        :param asunto:
        :param mensaje:
        :param url:
        :param usuarios:
        :return:
        """
        if usuarios:
            notificacion = Notificacion(asunto=asunto,
                                        mensaje=mensaje,
                                        url=url)
            notificacion.save()
            for usuario in usuarios:
                notificaion_usuario = NotificacionUsuario(notificacion=notificacion, usuario=usuario)
                notificaion_usuario.save()

    @staticmethod
    def get_datatable(notificacion_usuario_params):
        """
        Paginación datatable para las notificaciones
        :param notificacion_usuario_params:
        :return:
        """
        queryset = NotificacionUsuario.objects.filter(usuario=notificacion_usuario_params.request.user)
        notificacion_usuario_params.total = queryset.count()

        if notificacion_usuario_params.search_value:
            qset = Q()
            for sValue in notificacion_usuario_params.get_search_values():
                qset = qset & (
                        Q(notificacion__asunto__icontains=sValue) |
                        Q(notificacion__created_at__icontains=sValue))
            queryset = queryset.filter(qset)

        notificacion_usuario_params.count = queryset.count()
        notificacion_usuario_params.items = notificacion_usuario_params.init_items(queryset)

        return notificacion_usuario_params

    @staticmethod
    def html_email(notificacion):
        siaaf_url = settings.HOST_NAME
        return render_to_string('seguridad/notificacion/email.html', {'notificacion': notificacion, 'siaaf_url': siaaf_url})