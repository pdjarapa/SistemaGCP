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
from app.proyecto.domain.models import CasoPrueba, Proyecto, CicloPrueba, EjecucionPrueba
from app.proyecto.presentation.views.casos_forms import CasosForm
from app.proyecto.presentation.views.ciclos_forms import CicloForm
from app.proyecto.presentation.views.ejecucion_forms import EjecucionForm
from app.proyecto.presentation.views.proyecto_forms import ProyectoForm

app_service = CicloPruebaAppService()


class EjecucionPruebaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CicloPrueba
    template_name = 'ejecucionprueba/lista.html'
    permission_required = 'proyecto.view_cicloprueba'

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

    def get_context_data(self, **kwargs):
        self.cicloprueba = get_object_or_404(CicloPrueba, id=self.kwargs['ciclo_id'])
        self.proyecto = self.cicloprueba.proyecto

        context = super().get_context_data(**kwargs)

        context['cicloprueba'] = self.cicloprueba
        context['proyecto'] = self.proyecto

        context['title'] = 'Ejeución de ciclo de prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ('Detalle', None),
            ('Ciclos de prueba', None),
        ]

        return context

    def post(self, request, *args, **kwargs):
        data = app_service.get_datatable_ejecucion(request.POST)
        return JsonResponse(data, safe=False)

# class EjecucionPruebaCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
#     model = CicloPrueba
#     template_name = 'cicloprueba/crear.html'
#     permission_required = 'proyecto.add_cicloprueba'
#     form_class = CicloForm
#     success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."
#
#     def get_success_url(self):
#         return reverse('proyecto:cicloprueba_lista', args=[self.proyecto.id])
#
#     def form_valid(self, form):
#         self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
#         form.instance.proyecto = self.proyecto
#
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['proyecto_id'])
#         print('self.proyecto', self.proyecto)
#
#         context = super().get_context_data(**kwargs)
#
#         context['proyecto'] = self.proyecto
#         context['title'] = 'Crear ciclo prueba'
#         context['breadcrum'] = [
#             ('Proyectos', reverse('proyecto:proyecto_lista')),
#             ('Detalle', None),
#             ('Nuevo caso prueba', None)
#         ]
#
#         return context


class EjecucionPruebaUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EjecucionPrueba
    context_object_name = 'ejecucionprueba'
    template_name = 'ejecucionprueba/editar.html'
    permission_required = 'proyecto.change_ejecucionprueba'
    form_class = EjecucionForm
    success_message = "Estimado usuario, se ha registrado satisfactoriamente la información."

    def form_valid(self, form):
        self.ciclo_prueba = form.instance.ciclo_prueba

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('proyecto:cicloprueba_ejecutar', args=[self.object.ciclo_prueba.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ejecucionprueba = self.get_object()
        casoprueba = ejecucionprueba.caso_prueba
        proyecto = ejecucionprueba.caso_prueba.proyecto
        context['proyecto'] = proyecto
        context['cicloprueba'] = ejecucionprueba.ciclo_prueba
        context['title'] = 'Ejecutar caso de prueba'
        context['breadcrum'] = [
            ('Proyectos', reverse('proyecto:proyecto_lista')),
            ("Detalle", reverse('proyecto:proyecto_detalle', args=[proyecto.id])),
            ('Editar', None)
        ]
        return context

# class EjecucionPruebaDetailView(PermissionRequiredMixin, DetailView):
#     model = CicloPrueba
#     template_name = 'cicloprueba/detalle.html'
#     context_object_name = 'cicloprueba'
#     permission_required = 'proyecto.change_cicloprueba'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cicloprueba = self.get_object()
#         context['title'] = 'Detalle del proyecto'
#         context['breadcrum'] = [
#             ('Proyectos', reverse('proyecto:proyecto_lista')),
#             ("Detalle",)
#         ]
#         return context


@login_required
@permission_required('proyecto.change_cicloprueba', raise_exception=True, )
def agregar_caso_ejecutar(request, ciclo_id, caso_id):
    res = app_service.agregar_caso_prueba(ciclo_id, caso_id)
    return JsonResponse(res, safe=False)