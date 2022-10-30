import csv
import json
from datetime import datetime, timedelta

from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import ProtectedError, F, Value, Case, When, CharField
from django.db.models.aggregates import Sum
from django.db.models.functions import Concat, Coalesce
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.core.domain.dto.datatable import DataTableParams
from app.proyecto.application.proyecto_app_service import ProyectoAppService
from app.proyecto.domain.models import Proyecto
from app.proyecto.services.serializers import ProyectoSerializer
from app.seguridad.security.permissions import IsPermission


class ProyectoViewSet(viewsets.ViewSet):
    """
    API para las operaciones CRUD de proyectos
    """
    permission_classes = (IsAuthenticated,)

    @method_decorator(IsPermission('proyecto.view_proyecto'))
    def list(self, request):
        """
        Retorna un diccionario con la lista de productos, estado de la petición y mensaje.
        :param request:
        :return:
        """
        try:

            proyectos = ProyectoAppService.get_list()
            serializer = ProyectoSerializer(proyectos, many=True)

            return Response({'status': status.HTTP_200_OK,
                             'message': 'Respuesta con éxito',
                             'data': serializer.data})

        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': str(e),
                             'data': None})

    @method_decorator(IsPermission('proyecto.view_proyecto'))
    @action(detail=False)
    def get_list_datatable(self, request):
        """
        Retorna un diccionario con la lista de productos, estado de la petición y mensaje.
        :param request:
        :return:
        """
        params = DataTableParams(request, **request.GET)
        try:
            data_params = ProyectoAppService.get_datatable(params)
            serializer = ProyectoSerializer(data_params.items, many=True)
            result = params.result(serializer.data)
            return JsonResponse(result,
                                status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'detail': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @method_decorator(IsPermission('proyecto.delete_proyecto'))
    def destroy(self, request, pk=None):
        """
        Elimina el producto y retorna un diccionario con información de datos,
        estado de la petición y mensaje
        :param request:
        :param pk:
        :return:
        """
        try:
            proyecto = ProyectoAppService.delete(pk)
            return Response({'data': pk,
                             'status': status.HTTP_200_OK,
                             'message': "El producto {0} fue eliminado".format(proyecto.nombre.upper())
                             })
        except ProtectedError:
            msg = "El proyecto {0} no se puede eliminar".format(proyecto.nombre.upper())
            return Response({'status': status.HTTP_400_BAD_REQUEST,
                             'message': msg,
                             'data': None })

    @method_decorator(IsPermission('proyecto.add_proyecto'))
    def create(self, request):
        """
        Crea un objeto Producto y retorna información del producto creado,
        estado de la petición y mensaje
        :param request:
        :return:
        """
        try:
            r = ProyectoAppService.create(request.data)

            if not r.message:
                r['status'] = status.HTTP_200_OK
            else:
                r['status'] = status.HTTP_400_BAD_REQUEST

            return Response(r)

        except IntegrityError:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': 'El código %s ya existe para otro producto' % request.data['codigo']})

        except Exception as e:
            print(e)
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': str(e)})

    @method_decorator(IsPermission('proyecto.change_proyecto'))
    def update(self, request, pk=None):
        """
        Actualiza el objeto Producto, y retorna información del
        producto actualizado, estado de la petición y mensaje
        :param request:
        :param pk:
        :return:
        """
        try:


            proyecto = Proyecto.objects.get(id=pk)
            #producto.tipo_unidad_id = request.data['tipo_unidad'] if 'tipo_unidad' in request.data else None
            #producto.tipo_impuesto_id = request.data['tipo_impuesto'] if 'tipo_impuesto' in request.data else None

            serializer = ProyectoSerializer(proyecto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                producto_message = 'Item actualizado'
                producto_status = status.HTTP_200_OK
            else:
                producto_message = serializer.errors
                producto_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': producto_status,
                             'message': producto_message})



        except ObjectDoesNotExist as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': str(e)})

        except IntegrityError:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': 'El código %s ya existe para otro producto' % request.data['codigo']})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': str(e)})

