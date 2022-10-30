from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


class IsPermission(object):
    """
    Decorador que se ejecuta al consumir el API que valida si el usuario
    tienen el permiso para ejecutar una acción sobre le modelo. Ejemplo:
    @method_decorator(IsPermission('recaudacion.view_producto'))
    @method_decorator(IsPermission(('recaudacion.view_producto', 'recaudacion.change_producto')))
    """

    def __init__(self, permission):
        self.permission = permission

    def __call__(self, funcion):
        def wrapper(request, *args, **kwargs):
            try:
                perms = (self.permission,) if isinstance(self.permission, str) else self.permission
                if request.user.has_perms(perms) is False:
                    raise PermissionDenied
            except:
                raise PermissionDenied

            return funcion(request, *args, **kwargs)

        return wrapper