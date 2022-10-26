import os
from django.apps import apps
from django.conf import settings

from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.core.files.storage import FileSystemStorage


class DddAppDirectoriesFinder(AppDirectoriesFinder):
    """
    A static files finder that looks in the directory of each app as
    specified in the source_dir attribute.
    """

    storage_class = FileSystemStorage
    source_dir = "static"
    CUSTOM_APP_STATIC_DIR = getattr(settings, "CUSTOM_APP_STATIC_DIR", source_dir)
    CUSTOM_APP_STATIC_DIR_SRC = CUSTOM_APP_STATIC_DIR.replace('.', '/')

    def __init__(self, app_names=None, *args, **kwargs):
        # The list of apps that are handled
        self.apps = []
        # Mapping of app names to storage instances
        self.storages = {}
        app_configs = apps.get_app_configs()
        if app_names:
            app_names = set(app_names)
            app_configs = [ac for ac in app_configs if ac.name in app_names]
        for app_config in app_configs:
            app_storage = self.storage_class(
                os.path.join(app_config.path, self.source_dir)
            )

            app_storage_1 = self.storage_class(
                os.path.join(app_config.path, self.CUSTOM_APP_STATIC_DIR_SRC)
            )

            if os.path.isdir(app_storage.location):
                self.storages[app_config.name] = app_storage
                if app_config.name not in self.apps:
                    self.apps.append(app_config.name)

            #print('app_storage_1 c', app_storage_1.location)
            if os.path.isdir(app_storage_1.location):
                #print('app_storage_1', app_storage_1)
                self.storages[app_config.name] = app_storage_1
                if app_config.name not in self.apps:
                    self.apps.append(app_config.name)

        super().__init__(*args, **kwargs)