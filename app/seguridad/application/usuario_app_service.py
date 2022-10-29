import random
import string
import base64
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template.loader import get_template

#from app.configuracion.application.detalle_parametrizacion_app_service import DetalleParametrizacionAppService
from app.seguridad.domain.models import Funcionalidad, Usuario
#from app.asistencia.infraestructure.external.siaaf_app_service import SiaafAppService
#from app.tramite.models import Proceso

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
        def crear_persona(usuario, data_usuario):
            nueva_persona = Persona()
            nueva_persona.primer_apellido = data_usuario.get('primer_apellido', '')
            nueva_persona.segundo_apellido = data_usuario.get('segundo_apellido', '')
            nueva_persona.primer_nombre = data_usuario.get('primer_nombre', '')
            nueva_persona.segundo_nombre = data_usuario.get('segundo_nombre', '')
            nueva_persona.celular = data_usuario.get('celular', 'S/N')[:10]
            nueva_persona.fecha_nacimiento = data_usuario['fecha_nacimiento']
            nueva_persona.numero_documento = data_usuario['documento']
            nueva_persona.tipo_documento = data_usuario.get('tipo_documento', 1)
            nueva_persona.sexo = data_usuario.get('sexo', 1)
            nueva_persona.calle_principal = data_usuario.get('calle_principal', 'S/N')[:250]
            nueva_persona.calle_secundaria = data_usuario.get('calle_secundaria', 'S/N')[:250]
            nueva_persona.numero_casa = data_usuario.get('numero_casa', 'S/N')[:10]

            nueva_persona.save()
            usuario.persona = nueva_persona
            usuario.save()

        nuevo_usuario = Usuario.objects.filter(correo_electronico=data_usuario['correo_electronico']).first()

        if not nuevo_usuario:
            nuevo_usuario = Usuario()
            nuevo_usuario.activo = True
            nuevo_usuario.correo_electronico = data_usuario['correo_electronico']
            nuevo_usuario.acuerdo = True
            nuevo_usuario.password = ''
            nuevo_usuario.force_password = False

            crear_persona(nuevo_usuario, data_usuario)

            # usuario.password = make_password(solicitante['correo_electronico'])
        elif nuevo_usuario and nuevo_usuario.persona is None:
            crear_persona(nuevo_usuario, data_usuario)

        return nuevo_usuario

    @staticmethod
    def validar_correo_institucional(usuario, correo=None):
        """
        Valida el correo electronico
        :param correo:
        :return:
        """
        if not correo:
            correo = usuario.correo_electronico

        if correo.find('@unl.edu.ec') < 0:
            return False
        else:
            usuario.correo_electronico = correo
            return True


    @staticmethod
    def enviar_codigo_verificacion(usuario):
        subject = 'MGT-UNL Código de Verificación para el Módulo de Gestíón de trámites'
        template = get_template('autenticacion/envio_correo.html')

        content = template.render({
            'usuario': usuario,
        })
        destinatario = usuario.correo_electronico
        if not settings.PRODUCCION:
            destinatario = settings.EMAIL_TEST_RECEIVER

        message = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [destinatario])
        message.attach_alternative(content, 'text/html')
        mensaje = message.send()
        if mensaje == 1:
            return True
        return False

    @staticmethod
    def get_token(lenght=9):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(lenght))

    @staticmethod
    def iniciar_sesion_token(token):
        valido = False
        decodedBytes = base64.b64decode(token.encode("utf-8"))
        decodedBytes = base64.b64decode(decodedBytes)
        decodedStr = str(decodedBytes, "utf-8")
        cedula, fecha_nacimiento, id, fecha = decodedStr.split('|')
        usuario = Usuario.objects.filter(persona__numero_documento=cedula).first()
        proceso = Proceso.objects.filter(id=id).first()
        fecha_recibida = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S.%f')
        hoy = datetime.now()
        diferencia_fecha = hoy - fecha_recibida
        segundos = diferencia_fecha.days * 24 * 3600 + diferencia_fecha.seconds
        control_tiempo_token = DetalleParametrizacionAppService.get_valor_detalle_parametrizacion_codigo(
            'CONTROL_TIEMPO_TOKEN_SGA')
        if control_tiempo_token:
            if (segundos <= int(control_tiempo_token)) and usuario.persona.fecha_nacimiento == datetime.strptime(
                    fecha_nacimiento,
                    '%Y-%m-%d').date() and proceso:
                valido = True
        return usuario, proceso.id if proceso else None, valido


    @staticmethod
    def inicializar_usuario(usuario):
        if not usuario.descripcion or not usuario.identificacion:
            print('Incializar usuario --> %s' % usuario.correo_electronico)
            succes, data = SiaafAppService.consultar_datos_personales(usuario)
            #print (succes, data)
            if succes:
                #{'identificacion': '', 'mail': '', 'apellidos': '', 'nombres': '', 'telefono': '', 'password': b''}
                usuario.identificacion = data['identificacion']
                usuario.descripcion = ('%s %s' % (data['apellidos'], data['nombres']))
                usuario.save()

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
