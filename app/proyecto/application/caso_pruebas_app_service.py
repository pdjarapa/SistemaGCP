from django.db.models import Q

from app.core.application.BaseAppService import BaseAppService
from app.core.domain.dto.datatable import DataTableParams
from app.proyecto.domain.models import Proyecto, CasoPrueba, CicloPrueba
from app.proyecto.services.serializers import ProyectoSerializer


class CasoPruebaAppService(object):
    @staticmethod
    def get_datatable(filter_values):
        dtable = DataTableParams(filter_values)

        # Consulta
        proyecto_id = dtable.get('proyecto_id')
        ciclo_id = dtable.get('ciclo_id')
        print('proyecto_id',proyecto_id )
        print('ciclo_id', ciclo_id)

        qfilter = CasoPrueba.objects.filter(proyecto__id=proyecto_id)\
            #.annotate(tiempo_reconocido=Sum('asistencias__tiempo_reconocido', filter=Q(asistencias__estado=Asistencia.ESTADO_ACTIVO)))

        # Datatable - Calcula total, antes de aplicar filtros específicos
        dtable.total = qfilter.count()

        # Aplicar filtro (search)
        search_value = dtable.get_search_values()
        qset = Q()
        if search_value:
            for sValue in search_value:
                qset = qset & (Q(nombre__icontains=sValue) | Q(
                    descripcion__icontains=sValue))

        # En caso de pasar el ciclo, se quita los casos agregados
        if ciclo_id:
            c = CicloPrueba.objects.get(id=ciclo_id)
            cids = c.pruebas_ejecutadas.values_list('caso_prueba__id')
            qset = qset & ~Q(id__in=cids)

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
             'tipo': BaseAppService.get_choice_display(CasoPrueba.CHOICE_TIPO, it.tipo),
             'variedad': BaseAppService.get_choice_display(CasoPrueba.CHOICE_VARIEDAD, it.variedad),
             'prioridad': BaseAppService.get_choice_display(CasoPrueba.CHOICE_PRIORIDAD, it.prioridad),
             'evaluacion': BaseAppService.get_choice_display(CasoPrueba.CHOICE_EVALUACION, it.evaluacion),
             'estado': BaseAppService.get_choice_display(CasoPrueba.CHOICE_ESTADO, it.estado),
             'ciclos': it.pruebas_ejecutadas.count()
             }
            for it in dtable.init_items(qfilter)
        ]

        # Datatable - Obtiene resultado a retornar al cliente
        return dtable.result(data)