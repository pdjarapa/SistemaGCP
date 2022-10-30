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
        #empresa_codigo_sha = params.request.GET.get('empresa_sha')
        #empresa = EmpresaAppService.get_por_codigo_sha(empresa_codigo_sha)

        #estado, respuesta = RecaudacionSecService.usuario_acceso_empresa(params.request.user, empresa)
        #if estado:
        #import time
        #time.sleep(3)

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
             }
            for it in params.init_items(queryset)
        ]

        return params.result(data)


    def cambiar_estado(self, espacio_id, estado, request):
        proyecto = Proyecto.objects.get(id=espacio_id)

        proyecto.activo = estado
        proyecto.save()
        return {'status': 'ok', 'message': '¡Se cambió corretamente el estado!'}



