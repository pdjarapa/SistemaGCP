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

from app.seguridad.presentation.forms import EditarContrasenaForm
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
