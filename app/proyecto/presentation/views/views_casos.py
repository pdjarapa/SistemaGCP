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
from app.proyecto.domain.models import CasoPrueba, Proyecto
from app.proyecto.presentation.views.casos_forms import CasosForm
from app.proyecto.presentation.views.proyecto_forms import ProyectoForm

app_service = ProyectoAppService()

class CasoPruebaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = CasoPrueba
    template_name = 'casoprueba/crear.html'
    permission_required = 'proyecto.add_casoprueba'
    form_class = CasosForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def get_success_url(self):
        return reverse('proyecto:proyecto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Nuevo', None)
        ]
        return context

class CasoPruebaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CasoPrueba
    template_name = 'casoprueba/crear.html'
    permission_required = 'proyecto.change_casoprueba'
    form_class = CasosForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def get_success_url(self):
        return reverse('proyecto:proyecto_lista')

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

class CasoPruebaDetailView(PermissionRequiredMixin, DetailView):
    model = CasoPrueba
    template_name = 'casoprueba/detalle.html'
    context_object_name = 'casoprueba'
    permission_required = 'proyecto.change_casoprueba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto = self.get_object()
        context['title'] = 'Detalle del proyecto'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle",)
        ]
        return context
