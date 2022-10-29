from django.urls import include, path

app_name = 'seguridad'

urlpatterns = [
    path('', include('app.seguridad.services.urls.autenticacion')),
    path('', include('app.seguridad.services.urls.seguridad')),
]
