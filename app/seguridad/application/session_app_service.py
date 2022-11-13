from datetime import datetime, timedelta
from django.db.models import Q

from app.core.application.BaseAppService import BaseAppService
from app.core.domain.dto.datatable import DataTableParams
from app.seguridad.domain.models import SessionActivity, Usuario


class SessionAppService(BaseAppService):

    @staticmethod
    def get_dashboard():

        last30 = datetime.now() + timedelta(minutes=-30)

        data = {
            'total': SessionActivity.objects.count(),
            'total_30min': SessionActivity.objects.filter(login_at__gt = last30).count(),
            'usuarios': Usuario.objects.count(),
            'unicos': SessionActivity.objects.values('user').distinct().count(),
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

        queryset = SessionActivity.objects
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
             'user__descripcion': it.user.descripcion,
             'user__correo_electronico': it.user.correo_electronico,
             'ip_address_all': it.ip_address_all,
             'ip_address': it.ip_address,
             'user_agent': it.user_agent,
             'login_at': it.login_at.strftime(BaseAppService.DATETIME_FORMAT) if it.login_at else '',
             'logout_at': it.logout_at.strftime(BaseAppService.DATETIME_FORMAT) if it.logout_at else '',
             }
            for it in params.init_items(queryset)
        ]

        return params.result(data)