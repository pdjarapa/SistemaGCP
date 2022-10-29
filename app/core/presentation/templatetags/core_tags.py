"""
Tags a ser incluidos a nivel global
"""
from django import template
from django.apps import apps
from django.conf import settings

#from app.configuracion.domain.models import DetalleParametrizacion

register = template.Library()

@register.simple_tag
def system_name():
    return settings.SYSTEM_NAME

@register.simple_tag
def system_sname():
    return settings.SYSTEM_SNAME

@register.simple_tag
def system_alias():
    return settings.SYSTEM_ALIAS

@register.filter
def object_app_name(obj):
    return obj._meta.app_config.verbose_name

@register.filter
def object_verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def object_verbose_name_plural(obj):
    return obj._meta.verbose_name_plural

@register.filter
def verbose_name(clase):
    model = apps.get_model(clase)
    return model._meta.verbose_name


@register.filter
def verbose_name_plural(clase):
    model = apps.get_model(clase)
    return model._meta.verbose_name_plural

@register.simple_tag
def get_basehref():
    return '/%s' % settings.BASEHREF if settings.BASEHREF else ''