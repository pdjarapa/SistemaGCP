from django.db.models import Q

from app.core.domain.dto.datatable import DataTableParams
from app.proyecto.domain.models import Proyecto
from app.proyecto.services.serializers import ProyectoSerializer


class ProyectoAppService(object):

    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    @staticmethod
    def get_list():
        return Proyecto.objects.all()

    @staticmethod
    def delete(pk):
        proyecto = Proyecto.objects.get(id=pk)

    @staticmethod
    def create(data):
        proyecto = Proyecto()
        serializer = ProyectoSerializer(proyecto, data=data)

        if serializer.is_valid():
            serializer.save()
            return {'data': serializer.data, 'message': ''}
        else:
            return {'data': serializer.data, 'message': str('error', serializer.errors)}


    @staticmethod
    def get_datatable(filter_values):
        """
        Paginación datatable para proyectos
        :param params:
        :return:
        """

        params = DataTableParams(filter_values)

        queryset = Proyecto.objects
        params.total = queryset.count()

        qset = Q()
        if params.search_value:
            for i in params.get_search_values():
                qset = qset & (
                        Q(descripcion__icontains=i) |
                        Q(nombre__icontains=i)
                )

        activo = params.get_bool('filtro_activo')
        if activo is not None:
            qset = qset & Q(activo = activo)

        queryset = queryset.filter(qset)
        params.queryset = queryset
        params.count = queryset.count()

        # Datatable - Inicializa items
        data = [
            {'id': it.id,
             'nombre': it.nombre,
             'descripcion': it.descripcion,
             'activo': it.activo,
             'created_by': it.created_by,
             'created_at': it.created_at.strftime(ProyectoAppService.DATETIME_FORMAT),
             'casos': it.casos_prueba.count(),
             'ciclos': it.ciclos_prueba.count(),
             }
            for it in params.init_items(queryset)
        ]

        return params.result(data)


    def cambiar_estado(self, proyecto_id, estado, request):
        proyecto = Proyecto.objects.get(id=proyecto_id)

        proyecto.activo = estado
        proyecto.save()
        return {'status': 'ok', 'message': '¡Se cambió corretamente el estado!'}



