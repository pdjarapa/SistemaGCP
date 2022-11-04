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

from app.proyecto.application.caso_pruebas_app_service import CasoPruebaAppService
from app.proyecto.domain.models import CasoPrueba, Proyecto
from app.proyecto.presentation.views.casos_forms import CasosForm

app_service = CasoPruebaAppService()

class CasoPruebaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Proyecto
    template_name = 'casoprueba/lista.html'
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

    def get_context_data(self, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])

        context = super().get_context_data(**kwargs)

        context['proyecto'] = self.proyecto
        context['title'] = 'Casos de prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Detalle', None),
            ('Ciclos de prueba', None),
        ]

        return context

class CasoPruebaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CasoPrueba
    template_name = 'casoprueba/crear.html'
    permission_required = 'proyecto.add_casoprueba'
    form_class = CasosForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def get_success_url(self):
        return reverse('proyecto:casoprueba_lista', args=[self.proyecto.id])

    def form_valid(self, form):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
        form.instance.proyecto = self.proyecto

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
        print('self.proyecto', self.proyecto)

        context = super().get_context_data(**kwargs)

        context['casoprueba'] = self.proyecto
        context['title'] = 'Crear caso prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Detalle', None),
            ('Nuevo caso prueba', None)
        ]

        return context

class CasoPruebaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CasoPrueba
    context_object_name = 'casoprueba'
    template_name = 'casoprueba/crear.html'
    permission_required = 'proyecto.change_casoprueba'
    form_class = CasosForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def form_valid(self, form):
        self.proyecto = form.instance.proyecto
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('proyecto:casoprueba_lista', args=[self.proyecto.id])

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

class CasoPruebaDetailView(PermissionRequiredMixin, DetailView):
    model = CasoPrueba
    template_name = 'casoprueba/detalle.html'
    context_object_name = 'casoprueba'
    permission_required = 'proyecto.change_casoprueba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        casoprueba = self.get_object()
        context['title'] = 'Detalle del proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle",)
        ]
        return context
