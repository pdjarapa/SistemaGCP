from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404

from app.seguridad.application.log_app_service import LogAppService
from app.seguridad.application.session_app_service import SessionAppService


@login_required
def session_activity_lista(request):
    """
    Muestra todas las sessiones de usuario
    :param request:
    :return:
    """
    data = SessionAppService.get_dashboard()
    data['title'] = 'Sesiones de usuario'
    return render(request, 'dashboard/sessions.html', data)

@login_required
def session_activity_lista_paginador(request):
    """
    Lista de sessiones con la paginación de datatable
    :param request:
    :return:
    """
    try:
        data = SessionAppService.get_datatable(request.POST)
        return JsonResponse(data)
    except Exception as e:
        return HttpResponseServerError(e)


@login_required
def log_activity_lista(request):
    """
    Muestra todas las sessiones de usuario
    :param request:
    :return:
    """
    data = LogAppService.get_dashboard()
    data['title'] = 'Peticiones de usuarios'
    return render(request, 'dashboard/logs.html', data)

@login_required
def log_activity_lista_paginador(request):
    """
    Lista de sessiones con la paginación de datatable
    :param request:
    :return:
    """
    try:
        data = LogAppService.get_datatable(request.POST)
        return JsonResponse(data)
    except Exception as e:
        return HttpResponseServerError(e)