from django.apps import AppConfig

from ddd.config.clean_app_config import CleanAppConfig

class CoreConfig(CleanAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.core'

    # hf9SDD
    print('xx')
    run_already = True

    def ready(self):
        print('prev ready.')
        super().ready()
        print('post ready....')