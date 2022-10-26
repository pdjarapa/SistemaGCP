from importlib import import_module
from pkgutil import walk_packages

from django.apps import apps
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates
from django.template.backends.django import get_package_libraries, get_installed_libraries
from django.template.context import make_context
from django.template.engine import Engine
from django.template.library import InvalidTemplateLibrary




class DddTemplates(DjangoTemplates):

    def get_templatetag_libraries(self, custom_libraries):
        """
        Return a collation of template tag libraries from installed
        applications and the supplied custom_libraries argument.
        """
        libraries = _get_installed_libraries()
        libraries.update(custom_libraries)
        return libraries

def _get_installed_libraries():
    """
    Return the built-in template tag libraries and those from installed
    applications. Libraries are stored in a dictionary where keys are the
    individual module names, not the full module paths. Example:
    django.templatetags.i18n is stored as i18n.
    """
    return {
        module_name: full_name for module_name, full_name in _get_template_tag_modules()
    }


def _get_template_tag_modules():
    """
    Yield (module_name, module_path) pairs for all installed template tag
    libraries.
    """
    candidates = ["django.templatetags"]
    candidates.extend(
        f"{app_config.name}.templatetags" for app_config in apps.get_app_configs()
    )

    CUSTOM_APP_TEMPLATETAGS_DIR = getattr(settings, "CUSTOM_APP_TEMPLATETAGS_DIR", "")

    candidates.extend(
        f"{app_config.name}.{CUSTOM_APP_TEMPLATETAGS_DIR}" for app_config in apps.get_app_configs()
    )

    for candidate in candidates:
        try:
            #print('candiadet', candidate)
            pkg = import_module(candidate)
        except ImportError:
            # No templatetags package defined. This is safe to ignore.
            continue

        if hasattr(pkg, "__path__"):
            for name in get_package_libraries(pkg):
                yield name[len(candidate) + 1 :], name