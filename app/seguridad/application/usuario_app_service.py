import random
import string
import base64
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import get_template

from app.seguridad.domain.models import Funcionalidad, Usuario, NotificacionUsuario

class UsuarioAppService(object):

    @staticmethod
    def get_funcionalidad_hijas(funcionalidad, qset):
        """
        Devuelve una lista de funcionalidades hijas
        :param funcionalidad:
        :param qset: Para filtrar segun el modulo al que pertenece
        :return:
        """
        hijas = []
        for fun in funcionalidad.funcionalidades.filter(qset).distinct().order_by('orden').all():
            hijas.append({'nombre': fun.nombre,
                          'icon': fun.icon,
                          'formulario': fun.formulario,
                          'hijas': UsuarioAppService.get_funcionalidad_hijas(fun, qset)})
        return hijas

    @staticmethod
    def get_funcionalidades(usuario, modulo):
        """
        Retorna la funcionalidades del usuario ya sea django o angular
        :param modulo:
        :return:
        """
        if not usuario:
            return []
        qset = Q(funcionalidadesGroups__group__user=usuario, activo=True, modulo=modulo)
        respuesta = []
        funcionalidades_padre = Funcionalidad.objects.filter(qset, padre_id__isnull=True).distinct().order_by(
            'orden').all()
        for funcionalidad in funcionalidades_padre:
            respuesta.append({'nombre': funcionalidad.nombre,
                              'icon': funcionalidad.icon,
                              'formulario': funcionalidad.formulario,
                              'hijas': UsuarioAppService.get_funcionalidad_hijas(funcionalidad, qset)})

        return respuesta

    @staticmethod
    def get_nro_notificaciones(usuario):
        """
        Retorna el numero de notificaciones pendientes que tiene el usuario
        :param modulo:
        :return:
        """
        if not usuario:
            return 0
        return NotificacionUsuario.objects.filter(usuario=usuario, estado=NotificacionUsuario.ESTADO_PENDIENTE).count()

    @staticmethod
    def get_ultimas_notificaciones(usuario):
        """
        Retorna las ultimas 5 notificaciones del usuario
        :param modulo:
        :return:
        """
        if usuario:
            return NotificacionUsuario.objects.filter(usuario=usuario).order_by('-notificacion__created_at')[:10]
        else:
            return NotificacionUsuario.objects.none()

    @staticmethod
    def get_usuario(data_usuario):


        nuevo_usuario = Usuario.objects.filter(correo_electronico=data_usuario['correo_electronico']).first()

        if not nuevo_usuario:
            nuevo_usuario = Usuario()
            nuevo_usuario.activo = True
            nuevo_usuario.correo_electronico = data_usuario['correo_electronico']
            nuevo_usuario.acuerdo = True
            nuevo_usuario.password = ''
            nuevo_usuario.force_password = False

        return nuevo_usuario


    @staticmethod
    def crear_usuario(correo):
        """
        Crear el usuario si no existe, de lo contrario retorna el existente.
        """
        correo = correo.strip().lower()
        if not correo.endswith('@unl.edu.ec'):
            return False

        usuario = Usuario.objects.filter(correo_electronico=correo).first()
        if not usuario:
            usuario = Usuario()
            usuario.correo_electronico = correo
            usuario.activo = True
            #usuario.save()
            UsuarioAppService.inicializar_usuario(usuario)
        return usuario if (usuario.id and usuario.id > 0) else None
