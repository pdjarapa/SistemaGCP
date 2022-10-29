from django.apps import AppConfig
from django.db.models.signals import post_migrate

from ddd.config.clean_app_config import CleanAppConfig
from pathlib import Path


class SeguridadConfig(CleanAppConfig):
    name = 'app.seguridad'

    def ready(self):
        """
        Metodo ejecutado en cada carga del módulo Seguridad,
        se ejecuta metodo 'populate_models', para crear/actualizar grupos, funcionalidades, funcionalidades grupos y
        asignación de permisos a los grupos
        :return:
        """
        super().ready()
        #from ..seguridad.application import signals
        from ..seguridad.application import signals

        print('path: ', Path(self.path))

        #from app.core.application.signals import populate_models
        #post_migrate.connect(populate_models, sender=self)
    grupos = []
    funcionalidades = []