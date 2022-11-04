from django.db.models import Q

from app.core.application.BaseAppService import BaseAppService
from app.core.domain.dto.datatable import DataTableParams
from app.proyecto.domain.models import Proyecto, CasoPrueba, CicloPrueba, EjecucionPrueba
from app.proyecto.services.serializers import ProyectoSerializer


class CicloPruebaAppService(BaseAppService):

    @staticmethod
    def get_str_estado_caso_prueba(key):
        return BaseAppService.get_choice_display(CasoPrueba.CHOICE_ESTADO, key, '')
    @staticmethod
    def get_datatable(filter_values):
        dtable = DataTableParams(filter_values)

        # Consulta
        proyecto_id = dtable.get('proyecto_id')
        print('proyecto_id',proyecto_id )
        qfilter = CicloPrueba.objects.filter(proyecto__id=proyecto_id)\
            #.annotate(tiempo_reconocido=Sum('asistencias__tiempo_reconocido', filter=Q(asistencias__estado=Asistencia.ESTADO_ACTIVO)))

        # Datatable - Calcula total, antes de aplicar filtros específicos
        dtable.total = qfilter.count()

        # Aplicar filtro (search)
        search_value = dtable.get_search_values()
        if search_value:
            qset = Q()
            for sValue in search_value:
                qset = qset & (Q(nombre__icontains=sValue))
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
             'nombre': it.nombre,
             'descripcion': it.descripcion,
             }
            for it in dtable.init_items(qfilter)
        ]

        # Datatable - Obtiene resultado a retornar al cliente
        return dtable.result(data)

    @staticmethod
    def get_datatable_ejecucion(filter_values):
        dtable = DataTableParams(filter_values)

        # Consulta
        ciclo_id = dtable.get('ciclo_id')
        print('ciclo_id', ciclo_id)
        qfilter = EjecucionPrueba.objects.filter(ciclo_prueba__id=ciclo_id) \
            # .annotate(tiempo_reconocido=Sum('asistencias__tiempo_reconocido', filter=Q(asistencias__estado=Asistencia.ESTADO_ACTIVO)))

        # Datatable - Calcula total, antes de aplicar filtros específicos
        dtable.total = qfilter.count()

        # Aplicar filtro (search)
        search_value = dtable.get_search_values()
        #if search_value:
        #    qset = Q()
        #    for sValue in search_value:
        #        qset = qset & (Q(nombre__icontains=sValue))
        #    qfilter = qfilter.filter(qset)

        # Aplica filtro estado
        # activo = dtable.get('filtro_activo')
        # if activo:
        #    qfilter = qfilter.filter(activo=activo)

        # Datatable - Calcula total de registrados filtrados
        dtable.count = qfilter.count()

        # Datatable - Inicializa items
        data = [
            {'id': it.id,
             'caso_prueba__codigo': it.caso_prueba.codigo,
             'caso_prueba__nombre': it.caso_prueba.nombre,
             'caso_prueba__descripcion': it.caso_prueba.descripcion,
             'estado': CicloPruebaAppService.get_str_estado_caso_prueba(it.estado)
             }
            for it in dtable.init_items(qfilter)
        ]

        # Datatable - Obtiene resultado a retornar al cliente
        return dtable.result(data)

    @staticmethod
    def agregar_caso_prueba(ciclo_id,caso_id):
        ejecucion = EjecucionPrueba.objects.filter(ciclo_prueba_id=ciclo_id, caso_prueba_id=caso_id).first()
        if ejecucion:
            return {'status': 'error', 'message': '¡Ya existe este caso de prueba en el ciclo de pruebas!'}
        else:
            ejecucion = EjecucionPrueba(ciclo_prueba_id=ciclo_id, caso_prueba_id=caso_id)
            ejecucion.save()
            return {'status': 'ok', 'message': '¡Se agregó corretamente el caso de prueba!'}