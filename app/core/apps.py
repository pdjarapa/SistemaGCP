from django.apps import AppConfig

from ddd.config.clean_app_config import CleanAppConfig

class CoreConfig(CleanAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.core'
    run_already = True

    def ready(self):
        super().ready()