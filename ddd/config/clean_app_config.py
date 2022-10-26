from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.contrib.admin import site, AdminSite
from django.utils.module_loading import autodiscover_modules


class CleanAppConfig(AppConfig):
    """
    https://github.com/jdiazromeral/django-ddd
    https://github.com/jdiazromeral/django-ddd-quizs-demo/tree/main/src/service/infrastructure/controllers
    https://github.com/iktakahiro/dddpy
    https://github.com/programadorLhama/Backend-Python/tree/master/src
    https://github.com/CodelyTV/php-ddd-example
    https://github.com/patrick91/djangocon-eu-ddd
    https://github.com/cosmicpython/code/tree/3ed6ff0fab52e14edba6ced4b258af68c521115f/src/allocation

    https://www.geeksforgeeks.org/python-django-test-driven-development-of-web-api-using-drf-docker/

    https://www.youtube.com/watch?v=VzU9HdH3MZM
    https://download.microsoft.com/download/2/2/1/221AD022-E701-488F-B070-7A0B87DFE789/Guia_Arquitectura_N-Capas_DDD_NET_4_(Borrador_Marzo_2010).pdf

    """

    CUSTOM_MODELS_MODULE = getattr(settings, "CUSTOM_MODELS_MODULE", "models")
    CUSTOM_MIGRATIONS_MODULE = getattr(settings, "CUSTOM_MIGRATIONS_MODULE", "migrations")
    CUSTOM_ADMIN_MODULE = getattr(settings, "CUSTOM_ADMIN_MODULE", "admin")

    def import_models(self) -> None:
        super().import_models()
        self.__load_custom_models_module()

    def __load_custom_models_module(self) -> None:
        #print('module::::', f"{self.name}.{self.CUSTOM_MODELS_MODULE}")
        self.models_module = import_module(f"{self.name}.{self.CUSTOM_MODELS_MODULE}")

    def ready(self) -> None:
        self.__load_custom_admin_module(self.CUSTOM_ADMIN_MODULE, register_to=site)
        self.__load_custom_migration_module(self.CUSTOM_MIGRATIONS_MODULE)

    def __load_custom_admin_module(self, admin_module: str, register_to: AdminSite) -> None:
        autodiscover_modules(admin_module, register_to=register_to)

    def __load_custom_migration_module(self, migration_module: str) -> None:
        #print('migrations', f"{self.name}.{migration_module}")
        settings.MIGRATION_MODULES.update(**{self.label: f"{self.name}.{migration_module}"})
        #print(settings.MIGRATION_MODULES)
