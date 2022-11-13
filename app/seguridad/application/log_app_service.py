from datetime import datetime, timedelta
from django.db.models import Q

from app.core.application.BaseAppService import BaseAppService
from app.core.domain.dto.datatable import DataTableParams
from app.seguridad.domain.models import LogActivity, Usuario


class LogAppService(BaseAppService):

    @staticmethod
    def get_dashboard():

        last30 = datetime.now() + timedelta(minutes=-30)

        data = {
            'total': LogActivity.objects.count(),
            'total_pc': LogActivity.objects.filter(type=LogActivity.TIPO_PC).count(),
            'total_tablet': LogActivity.objects.filter(type=LogActivity.TIPO_TABLET).count(),
            'total_mobile': LogActivity.objects.filter(type=LogActivity.TIPO_MOBILE).count(),
        }

        return data;


    @staticmethod
    def get_datatable(filter_values):
        """
        Paginación datatable para proyectos
        :param params:
        :return:
        """

        params = DataTableParams(filter_values)

        queryset = LogActivity.objects
        params.total = queryset.count()

        qset = Q()
        if params.search_value:
            for i in params.get_search_values():
                qset = qset & (
                        Q(user__descripcion__icontains=i) |
                        Q(user__correo_electronico__icontains=i) |
                        Q(ip_address__icontains=i) |
                        Q(user_agent__icontains=i)
                )

        #activo = params.get_bool('filtro_activo')
        #if activo is not None:
        #    qset = qset & Q(activo = activo)

        queryset = queryset.filter(qset)
        params.queryset = queryset
        params.count = queryset.count()

        # Datatable - Inicializa items
        data = [
            {'id': it.id,
             'user__descripcion': it.user.descripcion if it.user else '',
             'user__correo_electronico': it.user.correo_electronico if it.user else '',
             'ip_address': it.ip_address,
             'user_agent': it.user_agent,
             'date': it.date.strftime(BaseAppService.DATETIME_FORMAT) if it.date else '',
             'type': it.get_type_display(),
             'system': it.system,
             'path': it.path,
             'method':it.method,
             'referer':it.referer,
             'browser': it.browser,
             'content_type': it.content_type,
             }
            for it in params.init_items(queryset)
        ]

        return params.result(data)