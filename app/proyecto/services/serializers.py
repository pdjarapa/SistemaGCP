from rest_framework import serializers

from app.proyecto.domain.models import Proyecto


class ProyectoSerializer(serializers.ModelSerializer):
    """
    Serializador para la clase Proyecto
    """

    class Meta:
        model = Proyecto
        #exclude = ('uaas', 'tipo_factura')
        fields = '__all__'