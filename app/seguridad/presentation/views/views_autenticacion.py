from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView

from app.seguridad.presentation.forms import EditarContrasenaForm, IniciarSesionSolicitanteForm
from app.seguridad.application import UsuarioAppService
from app.seguridad.domain.models import Usuario


@login_required
def cambiar_contrasena(request):
    """
    Cambia la contraseña del usuario logueado
    :param request:
    :return:
    """
    try:
        perfil = request.user.perfil
    except Exception as e:
        print('')

    form = EditarContrasenaForm
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if request.user.check_password('{}'.format(request.POST.get('actual_password'))):
            form.password_verificada()

        if form.is_valid():
            valor = form.cleaned_data['password']
            try:
                validate_password(valor, request.user)
            except ValidationError as e:
                form.add_error('password', e)
                return render(request, 'autenticacion/cambiar_contrasena.html', {'form': form})

            request.user.force_password = False
            request.user.password = make_password(valor)
            request.user.save()
            messages.success(request, "Datos actualizados correctamente... ")

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Por favor ingrese todos los datos... ")
    else:
        form = EditarContrasenaForm()
    return render(request, 'autenticacion/cambiar_contrasena.html', locals())


def cerrar_sesion(request):
    """
    Cerrar sesión del usuario logueado
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect('/')


def iniciar_sesion(request):
    """
    Verifica las credenciales e inicia sesión el usuario
    :param request:
    :return:
    """
    next = ""
    #SAC_URL = settings.SAC_URL
    # LDAP_ACTIVE = settings.LDAP_ACTIVE

    if request.GET:
        next = request.GET['next']

    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            correo_electronico = request.POST['username']
            usuario = Usuario.objects.filter(correo_electronico=correo_electronico).first()
            clave = request.POST['password']
            acceso = None

            if usuario:
                if usuario.activo:
                    acceso = authenticate(correo_electronico=correo_electronico, password=clave)

                    if acceso:
                        login(request, acceso)
                        if acceso.force_password:
                            return HttpResponseRedirect(reverse('seguridad:cambiar_contrasena'))
                        elif next == "":
                            return HttpResponseRedirect(reverse('index'))
                        else:
                            return HttpResponseRedirect(next)
                    else:
                        messages.warning(request, "Datos de acceso incorrectos. Usuario o contraseña incorrecta... ")
                else:
                    messages.warning(request, "Datos de acceso incorrectos. Usuario no está activo...")
            else:
                messages.warning(request, "Datos de acceso incorrectos. Usuario no existe... ")
    else:
        formulario = AuthenticationForm()

    return render(request, 'autenticacion/login.html', locals())


def iniciar_sesion_tipo_usuario(request):
    """
    Página para elegir que tipo de usuario es,
    si es usuario Solicitanto o es Funcionario
    """

    if request.user.is_authenticated:
        #return HttpResponse('<p>Welcome to <a href="https://djangocas.dev">django-cas-ng</a>.</p><p>You logged in as <strong>%s</strong>.</p><p><a href="/accounts/logout">Logout</a></p>' % request.user)
        return HttpResponseRedirect(reverse('index'))
    else:
        #return HttpResponse(
        #    '<p>Welcome to <a href="https://djangocas.dev">django-cas-ng</a>.</p><p><a href="/accounts/login">Login</a></p>')

        return render(request, 'autenticacion/iniciar_sesion_tipo_usuario.html', locals())


class InicioSesionSolicitante(FormView):
    # model = Solicitante
    # fields = ('correo_electronico', 'token', 'fecha_nacimiento', 'profesion',)
    form_class = IniciarSesionSolicitanteForm
    # success_url = reverse_lazy('tramite:inicio_sesion_solicitante')
    template_name = 'autenticacion/iniciar_sesion_solicitante.html'

    def post(self, request, *args, **kwargs):
        """ process user login"""
        if request.is_ajax():
            try:
                form = IniciarSesionSolicitanteForm(request.POST)
                if form.is_valid() and request.POST:
                    correo_electronico = request.POST.get('correo_electronico')
                    usuario = Usuario.objects.filter(correo_electronico=correo_electronico).first()
                    token = request.POST.get('token')
                    if not token:
                        return redirect('tramite:inicio_sesion_solicitante')

                    if Usuario.objects.filter(token=token, estado_token=Usuario.ESTADO_VALIDADO).exists():
                        token = request.POST.get('token')
                        # actualizamos datos con el nuevo token
                        usuario.password = token
                        usuario.token = token
                        usuario.estado_token = Usuario.ESTADO_OCUPADO
                        usuario.save()
                        #fecha_nacimiento = request.POST.get('fecha_nacimiento')
                        #profesion = request.POST.get('profesion')
                        #print(profesion)
                        #print(usuario.persona.profesion if usuario.persona else 'sin profesion')
                        # user = authenticate(correo_electronico_institucional=request.POST.get('correo_electronico'),
                        #                     password=token)
                        # user = usuario
                        if usuario is not None and usuario.is_active:
                            mensaje = "Usuario logeado correctamente"
                            error = "no hay error"
                            response = JsonResponse({'mensaje': mensaje, 'error': error})
                            response.status_code = 201
                            login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
                            return response
                mensaje = "No se ha podido iniciar sesion"
                error = form.errors
                response = JsonResponse({'mensaje': mensaje, 'error': error})
                response.status_code = 400
                return response
            except (KeyError, Persona.DoesNotExist):
                redirect('tramite:inicio_sesion_solicitante')
        else:
            return redirect('tramite:inicio_sesion_solicitante')


@method_decorator(csrf_exempt)
def registro_solicitante(request):
    persona = Persona.objects.filter(numero_documento=request.POST.get('numero_documento')).first()
    usuario = Usuario.objects.filter(correo_electronico=request.POST.get('correo_electronico')).first()
    form = RegistroSolicitanteForm(request.POST)

    BSG_API_URL = settings.BSG_API_URL
    print(request.POST)
    if request.POST:
        if form.is_valid():
            print("imprimio")
            usuario.acuerdo = True
            usuario.save()
            user = authenticate(correo_electronico=usuario.correo_electronico,
                                password=usuario.token)
            user = usuario
            user.activo = True
            user.save()
            login(request, user)
            return redirect('tramite:proceso_lista')
    # else:
    #     print(form.errors)
    print("aqui entro")
    # form = RegistroSolicitanteForm()
    return render(request, 'autenticacion/registro_solicitante.html', locals())


@method_decorator(csrf_exempt)
def verificar_persona(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # obtener el numero de documento de lado del cliente.
        numero_documento = request.GET.get("numero_documento", None)
        # verificar el número de documento en la base de datos.
        if Persona.objects.filter(numero_documento=numero_documento).exists():
            # si el numero de documento existe no puede crear un usuario
            return JsonResponse({"valido": False}, status=200)
        else:
            # si el numero de documento existe, el usuario puede crear un nuevo usuaio.
            return JsonResponse({"valido": True}, status=200)

    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def enviar_token(request):
    # obtenemos el token
    token = UsuarioAppService.get_token()
    usuario = Usuario.objects.filter(correo_electronico=request.POST.get('correo_electronico')).first()
    numero_documento = request.POST.get('numero_documento')
    if request.is_ajax() and request.POST:
        try:
            if usuario is None and numero_documento is None:
                return JsonResponse({'usuario_nuevo': True}, status=200)
            else:
                if usuario.correo_electronico and numero_documento is None:
                    usuario.password = token
                    usuario.token = token
                    usuario.save()
                    UsuarioAppService.enviar_codigo_verificacion(usuario)
                    return JsonResponse({'mensaje': MensajesEnum.ACCION_GUARDAR.value, "login": True})
                return JsonResponse({'error': "Esto es una error"}, status=400)
        except Exception as e:
            return JsonResponse({'error': "Esto es una error %s"%e}, status=400)


@require_http_methods(["POST"])
def verificar_token(request):
    # print(request.POST)
    if request.is_ajax() and request.POST:
        usuario = Usuario.objects.filter(
            correo_electronico=request.POST.get('correo_electronico')).first()
        token = request.POST.get('token', None)

        if Usuario.objects.filter(token=token).exists():
            # Cambio el estado del token a ocupado.
            usuario.estado_token = Usuario.ESTADO_VALIDADO
            usuario.save()
            return JsonResponse({"valido": False}, status=200)
        else:
            return JsonResponse({"valido": True}, status=200)

    return JsonResponse({}, status=400)
