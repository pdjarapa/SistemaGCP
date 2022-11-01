from django.db.models import Q

from app.core.domain.dto.datatable import DataTableParams
from app.proyecto.domain.models import Proyecto, CasoPrueba
from app.proyecto.services.serializers import ProyectoSerializer


class CasoPruebaAppService(object):
    @staticmethod
    def get_datatable(filter_values):
        dtable = DataTableParams(filter_values)

        # Consulta
        proyecto_id = dtable.get('proyecto_id')
        print('proyecto_id',proyecto_id )
        qfilter = CasoPrueba.objects.filter(proyecto__id=proyecto_id)\
            #.annotate(tiempo_reconocido=Sum('asistencias__tiempo_reconocido', filter=Q(asistencias__estado=Asistencia.ESTADO_ACTIVO)))

        # Datatable - Calcula total, antes de aplicar filtros específicos
        dtable.total = qfilter.count()

        # Aplicar filtro (search)
        search_value = dtable.get_search_values()
        if search_value:
            qset = Q()
            for sValue in search_value:
                qset = qset & (Q(nombre__icontains=sValue) | Q(
                    descripcion__icontains=sValue))
            qfilter = qfilter.filter(qset)

        # Aplica filtro estado
        #activo = dtable.get('filtro_activo')
        #if activo:
        #    qfilter = qfilter.filter(activo=activo)

        # Datatable - Calcula total de registrados filtrados
        dtable.count = qfilter.count()

        # Datatable - Inicializa items
        data = [
            {'id': it.id,
             'codigo': it.codigo,
             'nombre': it.nombre,
             'descripcion': it.descripcion,
             }
            for it in dtable.init_items(qfilter)
        ]

        # Datatable - Obtiene resultado a retornar al cliente
        return dtable.result(data)