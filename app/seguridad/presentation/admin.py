from django.contrib import admin

from app.seguridad.domain.models import Funcionalidad, SessionActivity
from app.seguridad.domain.models import FuncionalidadGroup
from app.seguridad.domain.models import Usuario

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class AuditModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = str(request.user)
        obj.updated_by = str(request.user)
        obj.save()


class FuncionalidadAdmin(admin.ModelAdmin):
    fields = (
    'nombre', 'formulario', 'orden', 'padre', 'codigo', 'activo', 'mostrar', 'icon', 'descripcion', 'modulo',)
    list_filter = ('modulo', 'activo',)
    search_fields = ('nombre',)
    list_display = ('codigo', 'nombre', 'formulario', 'icon', 'orden', 'padre')
    list_display_links = ('codigo', 'nombre',)
    list_per_page = 25


class FuncionalidadGrupoAdmin(admin.ModelAdmin):
    fields = ('funcionalidad', 'group',)
    search_fields = ('funcionalidad__nombre','group__name')
    list_display = ('funcionalidad', 'group')
    list_per_page = 25


class PersonaAdmin(admin.ModelAdmin):
    # fields = ('numero_documento', 'primer_apellido', 'primer_nombre',)
    search_fields = ('numero_documento', 'primer_apellido')
    list_display = ('numero_documento', 'primer_apellido', 'primer_nombre')
    list_per_page = 25


class UsuarioAdmin(BaseUserAdmin):
    readonly_fields = ('last_login',)
    list_filter = ('activo', 'is_admin', 'force_password', 'groups')
    list_display = ('correo_electronico', 'last_login', 'activo', 'descripcion')
    search_fields = ('correo_electronico', )
    ordering = ('correo_electronico',)
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo_electronico', 'password1', 'password2'),
        }),
    )

class SessionActivityAdmin(admin.ModelAdmin):
    list_display = ('user','session_key','login_at', 'logout_at', 'ip_address', 'ip_address_all', 'user_agent')
    search_fields = ('user__nombre_de_usuario', 'user__persona__numero_documento', 'ip_address', 'ip_address_all')
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Funcionalidad, FuncionalidadAdmin)
admin.site.register(FuncionalidadGroup, FuncionalidadGrupoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(SessionActivity, SessionActivityAdmin)
