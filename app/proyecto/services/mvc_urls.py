from django.urls import path
from app.proyecto.presentation.views import views_proyecto

app_name = 'proyecto'

urlpatterns = [
    path('proyecto/lista', views_proyecto.ProyectoListView.as_view(), name='proyecto_lista'),
    path('proyecto/crear', views_proyecto.ProyectoCreateView.as_view(), name='proyecto_crear'),
    path('proyecto/editar/<int:pk>', views_proyecto.ProyectoUpdateView.as_view(), name='proyecto_editar'),
    path('proyecto/detalle/<int:pk>', views_proyecto.ProyectoDetailView.as_view(), name='proyecto_detalle'),
    path('proyecto/activar/<int:id>', views_proyecto.activar_espacio, name='proyecto_activar'),
    path('proyecto/desactivar/<int:id>', views_proyecto.desactivar_espacio, name='proyecto_desactivar'),
]
