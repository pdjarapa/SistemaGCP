from django.db import models
from app.seguridad.security.middleware import get_username
from datetime import datetime

# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True

class AuditModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(max_length=50, verbose_name='Creado por', null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=50, verbose_name='Actualizado por', null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        req = get_username()
        if req:
            if not self.pk:
                self.created_by = str(req.user)

            self.updated_by = str(req.user)
            self.updated_at = datetime.today()

        super(AuditModel, self).save(*args, **kwargs)

class Xyz(BaseModel):
    created_atxx = models.DateTimeField(auto_now_add=True, null=True)