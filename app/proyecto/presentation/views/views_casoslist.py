from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView

from app.proyecto.application.caso_pruebas_app_service import CasoPruebaAppService
from app.proyecto.application.proyecto_app_service import ProyectoAppService
from app.proyecto.domain.models import Proyecto
from app.proyecto.presentation.views.proyecto_forms import ProyectoForm

app_service = CasoPruebaAppService()

class CasoPruebaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyecto/lista.html'
    permission_required = 'proyecto.view_casoprueba'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if not self.request.is_ajax():
            return super().handle_no_permission()
        return JsonResponse({
            'status': 'error',
            'message': 'Su sesión ha caducado, es necesario volver a inicar sesión para acceder a esta sección.'
        }, status=401)

    def post(self, request, *args, **kwargs):
        data = app_service.get_datatable(request.POST)
        return JsonResponse(data, safe=False)

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['title'] = 'Lista de proyectos'
    #    context['breadcrum'] = [('Proyectos', reverse('proyecto:proyecto_lista'))]
    #    return context