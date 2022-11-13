# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib import admin
from app.seguridad.presentation.views import views_seguridad

admin.autodiscover()

urlpatterns = [
    path('dashboard/sesiones', views_seguridad.session_activity_lista, name='dashboard_sessions'),
    path('dashboard/sesiones/paginator', views_seguridad.session_activity_lista_paginador, name='dashboard_sessions_paginator'),
]
