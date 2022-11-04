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


class CasoPrueba(AuditModel):
    TIPO_FUNCIONAL = 'F'
    TIPO_NO_FUNCIONAL = 'N'
    TIPO_ESTRUCTURAL = 'E'
    TIPO_REGRESION = 'R'

    VARIEDAD_POSITVA = '+'
    VARIEDAD_NEGATIVA = '-'

    PIORIDAD_ALTA = 'A'
    PIORIDAD_MEDIA = 'M'
    PIORIDAD_BAJA = 'B'

    EVALUACION_MANUAL = 'M'
    EVALUACION_AUTOMATICA = 'A'

    ESTADO_BORRADOR = 'B'
    ESTADO_APROBADA = 'A'
    ESTADO_BLOQUEADA = 'L'
    ESTADO_FALLO = 'F'

    CHOICE_TIPO = (
    (TIPO_FUNCIONAL, 'Funcional'), (TIPO_NO_FUNCIONAL, 'No Funcional'), (TIPO_ESTRUCTURAL, 'Estructural'),
    (TIPO_REGRESION, 'Regresión'))
    CHOICE_VARIEDAD = ((VARIEDAD_POSITVA, 'Positiva'), (VARIEDAD_NEGATIVA, 'Negativa'))
    CHOICE_PRIORIDAD = ((PIORIDAD_ALTA, 'Alta'), (PIORIDAD_MEDIA, 'Media'), (PIORIDAD_BAJA, 'Baja'))
    CHOICE_EVALUACION = ((EVALUACION_MANUAL, 'Manual'), (EVALUACION_AUTOMATICA, 'Automática'))
    CHOICE_ESTADO = ((ESTADO_BORRADOR, 'Borrador'), (ESTADO_BLOQUEADA, 'Bloqueda'), (ESTADO_APROBADA, 'Aprobada'),
                     (ESTADO_FALLO, 'Fallo'))

    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(max_length=250, null=True, blank=True)
    precondicion = models.TextField(max_length=250, null=True, blank=True)
    pasos = models.TextField(max_length=250, null=True, blank=True)
    resultado_esperado = models.TextField(max_length=250, null=True, blank=True)
    postcondicion = models.TextField(max_length=250, null=True, blank=True)
    observacion = models.TextField(max_length=250, null=True, blank=True)

    tipo = models.CharField(max_length=1, choices=CHOICE_TIPO, default=TIPO_FUNCIONAL)
    variedad = models.CharField(max_length=1, choices=CHOICE_VARIEDAD, default=VARIEDAD_POSITVA)
    prioridad = models.CharField(max_length=1, choices=CHOICE_PRIORIDAD, default=PIORIDAD_BAJA)
    evaluacion = models.CharField(max_length=1, choices=CHOICE_EVALUACION, default=EVALUACION_MANUAL)
    estado = models.CharField(max_length=1, choices=CHOICE_ESTADO, default=ESTADO_BORRADOR)

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='casos_prueba')

    class Meta:
        ordering = ('codigo',)
        constraints = [models.UniqueConstraint(fields=['codigo', 'proyecto'], name='caso_prueba_codigo_proyecto_unique')]

    def __str__(self):
        return '%s' % (self.codigo)


class CicloPrueba(AuditModel):
    nombre = models.TextField(max_length=80)
    descripcion = models.TextField(max_length=250, null=True, blank=True)

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ciclos_prueba')

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return '%s' % (self.nombre)


class EjecucionPrueba(AuditModel):
    ciclo_prueba = models.ForeignKey(CicloPrueba, on_delete=models.CASCADE, related_name='pruebas_ejecutadas')
    caso_prueba = models.ForeignKey(CasoPrueba, on_delete=models.CASCADE, related_name='pruebas_ejecutadas')
    estado = models.CharField(max_length=1, choices=CasoPrueba.CHOICE_ESTADO, default=CasoPrueba.ESTADO_BORRADOR)
    comentario = models.TextField(max_length=250, null=True, blank=True)
    evidencia = models.ImageField(upload_to='evidencia/%Y/%m/%d/')