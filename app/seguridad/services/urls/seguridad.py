# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib import admin
from app.seguridad.presentation.views import views_seguridad

admin.autodiscover()

urlpatterns = [
    path('notificacion-usuario/detalle/<int:id>', views_seguridad.notificacion_usuario_detalle, name='notificacion_usuario_detalle'),
    path('notificacion-usuario/lista', views_seguridad.notificacion_usuario_lista, name='notificacion_usuario_lista'),
    path('notificacion-usuario/lista-paginador', views_seguridad.notificacion_usuario_lista_paginador, name='notificacion_usuario_lista_paginador'),
]
