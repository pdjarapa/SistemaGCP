from django.db import models

from app.core.domain.models import AuditModel
from app.seguridad.security.middleware import get_username
from datetime import datetime

# Create your models here.


class Proyecto(AuditModel):
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=250, verbose_name="Descripción")
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('nombre',)
        unique_together = ('nombre',)

    def __str__(self):
        return '%s' % (self.nombre)