from django.apps import AppConfig

from ddd.config.clean_app_config import CleanAppConfig

class ProyectosConfig(CleanAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.proyecto'

    #run_already = True

    def ready(self):
        super().ready()