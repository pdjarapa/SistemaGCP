from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView

from app.proyecto.application.ciclo_pruebas_app_service import CicloPruebaAppService
from app.proyecto.application.proyecto_app_service import ProyectoAppService
from app.proyecto.domain.models import CasoPrueba, Proyecto, CicloPrueba
from app.proyecto.presentation.views.casos_forms import CasosForm
from app.proyecto.presentation.views.ciclos_forms import CicloForm
from app.proyecto.presentation.views.proyecto_forms import ProyectoForm

app_service = CicloPruebaAppService()


class CicloPruebaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Proyecto
    template_name = 'cicloprueba/lista.html'
    permission_required = 'proyecto.view_cicloprueba'

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if not self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return super().handle_no_permission()
        return JsonResponse({
            'status': 'error',
            'message': 'Su sesión ha caducado, es necesario volver a inicar sesión para acceder a esta sección.'
        }, status=401)

    def get_context_data(self, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])

        context = super().get_context_data(**kwargs)

        context['proyecto'] = self.proyecto
        context['title'] = 'Ciclos de prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Detalle', None),
            ('Ciclos de prueba', None),
        ]

        return context

    def post(self, request, *args, **kwargs):
        data = app_service.get_datatable(request.POST)
        return JsonResponse(data, safe=False)

class CicloPruebaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CicloPrueba
    template_name = 'cicloprueba/crear.html'
    permission_required = 'proyecto.add_cicloprueba'
    form_class = CicloForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def get_success_url(self):
        return reverse('proyecto:cicloprueba_lista', args=[self.proyecto.id])

    def form_valid(self, form):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
        form.instance.proyecto = self.proyecto

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
        print('self.proyecto', self.proyecto)

        context = super().get_context_data(**kwargs)

        context['proyecto'] = self.proyecto
        context['title'] = 'Crear ciclo prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Detalle', None),
            ('Nuevo caso prueba', None)
        ]

        return context

class CicloPruebaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CicloPrueba
    context_object_name = 'cicloprueba'
    template_name = 'cicloprueba/crear.html'
    permission_required = 'proyecto.change_cicloprueba'
    form_class = CicloForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def form_valid(self, form):
        self.proyecto = form.instance.proyecto
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('proyecto:cicloprueba_lista', args=[self.proyecto.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        casoprueba = self.get_object()
        proyecto = casoprueba.proyecto
        context['proyecto'] = proyecto
        context['title'] = 'Editar caso de prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle", reverse('proyecto:proyecto_detalle', args=[proyecto.id])),
            ('Editar', None)
        ]
        return context

class CicloPruebaDetailView(PermissionRequiredMixin, DetailView):
    model = CicloPrueba
    template_name = 'cicloprueba/detalle.html'
    context_object_name = 'cicloprueba'
    permission_required = 'proyecto.change_cicloprueba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cicloprueba = self.get_object()
        context['title'] = 'Detalle del proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle",)
        ]
        return context
