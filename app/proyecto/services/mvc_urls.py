from django.urls import path
from app.proyecto.presentation.views import views_casos, views_proyecto, views_ciclos

app_name = 'proyecto'

urlpatterns = [
    path('proyecto/lista', views_proyecto.ProyectoListView.as_view(), name='proyecto_lista'),
    path('proyecto/crear', views_proyecto.ProyectoCreateView.as_view(), name='proyecto_crear'),
    path('proyecto/editar/<int:pk>', views_proyecto.ProyectoUpdateView.as_view(), name='proyecto_editar'),
    path('proyecto/detalle/<int:pk>', views_proyecto.ProyectoDetailView.as_view(), name='proyecto_detalle'),
    path('proyecto/activar/<int:id>', views_proyecto.activar_proyecto, name='proyecto_activar'),
    path('proyecto/desactivar/<int:id>', views_proyecto.desactivar_proyecto, name='proyecto_desactivar'),

    path('caso_prueba/lista/<int:proyecto_id>', views_casos.CasoPruebaListView.as_view(), name='casoprueba_lista'),
    path('caso_prueba/crear/<int:proyecto_id>', views_casos.CasoPruebaCreateView.as_view(), name='casoprueba_crear'),
    path('caso_prueba/editar/<int:pk>', views_casos.CasoPruebaUpdateView.as_view(), name='casoprueba_editar'),

    path('ciclo_prueba/lista/<int:proyecto_id>', views_ciclos.CicloPruebaListView.as_view(), name='cicloprueba_lista'),
    path('ciclo_prueba/crear/<int:proyecto_id>', views_ciclos.CicloPruebaCreateView.as_view(), name='cicloprueba_crear'),
    path('ciclo_prueba/editar/<int:pk>', views_ciclos.CicloPruebaUpdateView.as_view(), name='cicloprueba_editar'),
]
