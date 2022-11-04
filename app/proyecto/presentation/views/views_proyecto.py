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


from app.proyecto.application.proyecto_app_service import ProyectoAppService
from app.proyecto.domain.models import Proyecto
from app.proyecto.presentation.views.proyecto_forms import ProyectoForm

app_service = ProyectoAppService()

class ProyectoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyecto/lista.html'
    permission_required = 'proyecto.view_proyecto'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de proyectos'
        context['breadcrum'] = [('Proyectos', reverse('proyecto:proyecto_lista'))]
        return context

class ProyectoCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proyecto
    template_name = 'proyecto/crear.html'
    permission_required = 'proyecto.add_proyecto'
    form_class = ProyectoForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def get_success_url(self):
        return reverse('proyecto:proyecto_detalle', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Nuevo', None)
        ]
        return context

class ProyectoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proyecto
    template_name = 'proyecto/crear.html'
    permission_required = 'proyecto.change_proyecto'
    form_class = ProyectoForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def get_success_url(self):
        return reverse('proyecto:proyecto_detalle', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()
        context['title'] = 'Editar proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle", reverse('proyecto:proyecto_detalle', args=[proyecto.id])),
            ('Editar', None)
        ]
        return context

class ProyectoDetailView(PermissionRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto/detalle.html'
    context_object_name = 'proyecto'
    permission_required = 'proyecto.change_proyecto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()
        context['title'] = 'Detalle del proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle",)
        ]
        return context


@login_required
@permission_required('proyecto.change_proyecto', raise_exception=True, )
def activar_proyecto(request, id):
    res = app_service.cambiar_estado(id, True, request)
    return JsonResponse(res, safe=False)

@login_required
@permission_required('proyecto.change_proyecto', raise_exception=True, )
def desactivar_proyecto(request, id):
    res = app_service.cambiar_estado(id, False, request)
    return JsonResponse(res, safe=False)

