# -*- coding: utf-8 -*-
"""
Django settings for cfg project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.apps import apps
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR', BASE_DIR)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SYSTEM_NAME = "Sistema de Gestión de Casos de Prueba"
SYSTEM_SNAME = "Sistema GCP"
SYSTEM_ALIAS = "GCP"

# Configuración n-layer architecture
CUSTOM_MODELS_MODULE = "domain.models"
CUSTOM_MIGRATIONS_MODULE = "infraestructure.migrations"
CUSTOM_ADMIN_MODULE = "presentation.admin"
CUSTOM_APP_TEMPLATETAGS_DIR = "presentation.templatetags"
CUSTOM_APP_TEMPLATE_DIR =  "presentation" + os.sep + "templates"
CUSTOM_APP_STATIC_DIR = "presentation" + os.sep + "static"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_zs9t)koy41f$!8vrwy#5(vvzuu+q$&lj%a80_le7oiu6!zq&3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'seguridad.Usuario'
LOGIN_URL= '/seguridad/accounts/login'

# Application definition
CUSTOM_INSTALLED_APPS = [
    'app.core.apps.CoreConfig',
    'app.seguridad.apps.SeguridadConfig',
    'app.proyecto.apps.ProyectosConfig'
]

LIB_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auditlog',
    'rest_framework',
    'crispy_forms'
]

INSTALLED_APPS = LIB_INSTALLED_APPS + CUSTOM_INSTALLED_APPS

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'app.seguridad.security.middleware.RequestMiddleware',
    'app.seguridad.security.middleware.RemoteUserMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'cfg.urls'

TEMPLATES_DIRS = ['templates', os.path.join(BASE_DIR / 'presentation' / 'templates')]
for app in CUSTOM_INSTALLED_APPS:
    apath = app.split('.')
    app_templates = os.path.join(BASE_DIR, apath[0], apath[1], CUSTOM_APP_TEMPLATE_DIR)
    TEMPLATES_DIRS.append(app_templates)

TEMPLATES = [
    {
        'BACKEND': 'ddd.template.finder.DddTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['app.core.presentation.templatetags.core_tags'],
        },
    },
]

WSGI_APPLICATION = 'cfg.wsgi.application'


 #Database
 #https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'OPTIONS': {
          'options': '-c search_path=django,public'
      },
      'NAME': 'gpc',
      'USER': 'sgcp@siscaspru-dbpos',
      'PASSWORD': 'Desarrollo1',
      'HOST': 'siscaspru-dbpos.postgres.database.azure.com',
      'PORT': '5432',

  },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
#USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'ddd.static.finder.DddAppDirectoriesFinder',
]

for app in CUSTOM_INSTALLED_APPS:
    apath = app.split('.')
    app_static = os.path.join(BASE_DIR, apath[0], apath[1], CUSTOM_APP_STATIC_DIR)
    #print('app_static', app_static)
    STATICFILES_DIRS.append(app_static)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
