from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from ..services import api_views

router = DefaultRouter(trailing_slash=False)
router.register(r'proyectos', api_views.ProyectoViewSet, basename='proyecto')

urlpatterns = [
    path('', include(router.urls)),
]