# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.core.application.core_app_service import CoreAppService
from app.core.domain.models import AuditModel


class ManejadorUsuarios(BaseUserManager):
    # use_in_migrations = True

    def _create_user(self, correo_electronico, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not correo_electronico:
            raise ValueError('Usuario debe tener un correo válido.')
        correo_electronico = self.normalize_email(correo_electronico)
        user = self.model(correo_electronico=correo_electronico, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, correo_electronico, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(correo_electronico, password, **extra_fields)

    def create_superuser(self, correo_electronico, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('activo', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario tiene que tener is_superuser=True.')

        return self._create_user(correo_electronico, password, **extra_fields)

class LogActivity(models.Model):
    TIPO_OTHER = 'O'
    TIPO_MOBILE = 'M'
    TIPO_TABLET = 'T'
    TIPO_PC = 'P'

    CHOICE_TIPO = ((TIPO_MOBILE, 'Mobile'), (TIPO_TABLET, 'Tablet'), (TIPO_PC, 'Pc'))

    date = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=80, null=True)
    method = models.CharField(max_length=8, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(null=True)
    system = models.CharField(max_length=20, null=True)
    browser = models.TextField(max_length=20, null=True)
    type = models.CharField(max_length=1, choices=CHOICE_TIPO, default=TIPO_OTHER)
    path = models.TextField(null=True)
    referer = models.TextField(null=True)
    is_ajax = models.BooleanField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class SessionActivity(models.Model):

    login_at = models.DateTimeField(auto_now_add=True)
    logout_at = models.DateTimeField(null=True)
    session_key = models.CharField(_("session key"), max_length=40)
    user_agent = models.TextField(null=True)
    ip_address = models.GenericIPAddressField(null=True)
    ip_address_all = models.TextField(null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Session activity")
        verbose_name_plural = _("Session activity")

    @staticmethod
    def create_session_activity(request, user, **kwargs):
        """
        Start session activity tracking for newly logged-in user.
        """
        session = request.session

        if user.is_authenticated and session.session_key:
            ip_address_all = CoreAppService.get_request_ip_all(request)
            request.META['REMOTE_ADDR'] = CoreAppService.get_request_ip(request)

            SessionActivity.objects.get_or_create(
                user=user,
                session_key=session.session_key,
                ip_address=request.META.get("REMOTE_ADDR", None),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                ip_address_all=ip_address_all
            )

    @staticmethod
    def end_session_activity(request, user, **kwargs):
        """
        Marks end of the session activity.
        Should be called when user logs out or when a session is deactivated.
        """
        session_key = request.session.session_key
        if session_key:
            SessionActivity.objects.filter(session_key=session_key).update(
                logout_at=datetime.now()
            )


class Usuario(AbstractBaseUser, PermissionsMixin, AuditModel):

    activo = models.BooleanField(default=False)
    correo_electronico = models.EmailField(unique=True, blank=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)

    force_password = models.BooleanField(default=True)  # Forzar cambio de contraseña
    # foto_url = models.TextField(blank=True, max_length=7000, null=True)
    # google = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # ldap = models.BooleanField(default=False)


    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = []

    objects = ManejadorUsuarios()

    class Meta:
        ordering = ['correo_electronico']

    def __str__(self):
        return self.correo_electronico

    def is_staff(self):
        """
        Requerido pora ingresar al admin de django, valida si es admin
        :return:
        """
        return self.is_admin

    def get_display_name(self):
        return self.descripcion if self.descripcion else self.correo_electronico

user_logged_in.connect(SessionActivity.create_session_activity)
user_logged_out.connect(SessionActivity.end_session_activity)
