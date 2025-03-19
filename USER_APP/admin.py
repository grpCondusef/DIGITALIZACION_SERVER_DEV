from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Bitacora  # IMPORTAMOS NUESTROS MODELOS AL PANEL DE ADMINISTRACIÓN

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name','last_name','is_active', 'area', 
                    'crear_expedientes', 'eliminar_expedientes','subir_documentos', 'consulta_completa', 'migrar_expediente', 'carga_masiva', 'eliminar_documentos',)  # CAMPOS QUE APARECEN EN LA TABLA DE REGISTROS
    ordering = ('username','area',)
    search_fields = ('username', 'first_name','last_name',)
    autocomplete_fields = ['area'] #AUTOCOMPLETADO DE ÁREAS PARA FACILITAR ENCONTRARLAS
    
    filter_horizontal = ['areas_asociadas']

class BitacoraAdmin(admin.ModelAdmin):
    list_display= ('user', 'action', 'description', 'expediente', 'date')
    search_fields = ('user__username', 'expediente__clave',)


admin.site.register(User, UserAdmin)
admin.site.register(Bitacora,   BitacoraAdmin)
