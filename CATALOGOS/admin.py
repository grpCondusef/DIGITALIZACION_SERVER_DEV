from django.contrib import admin
from CATALOGOS.models import InstitucionesFinancieras, EstatusCatalogo, TipoDocumental, TipoMacroproceso, Macroproceso, Areas, AreaSIO, Serie, TipoOrdenamiento, Proceso, AreaProcedenciaN, EstatusExpediente, Expediente, ExpedienteOptions


class InstitucionesFinancierasAdmin(admin.ModelAdmin):
    list_display = ('clave_registro', 'denominacion_social',
                    'nombre_corto', 'estatus',)
    ordering = ('nombre_corto',)  # DEBE ESTAR DEFINIDO PARA EL AUTOCOMPLETADO

    search_fields = ('denominacion_social',)


class EstatusCatalogoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


class TipoDocumentalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'clave', )


class TipoMacroprocesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fechaInicio', 'fechaFin',
                    'fechaActualizacion', 'idEstatus',)
    ordering = ('nombre',)


class MacroprocesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'idTipoMacroproceso', 'fechaInicio', )
    ordering = ('nombre',)


class ProcesoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'idMacroproceso', 'fechaInicio', )
    ordering = ('nombre',)


class TipoOrdenamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', )
    ordering = ('nombre',)


class AreasAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)


class AreaSIOAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fechaInicio', 'fechaActualizacion',)
    ordering = ('nombre',)


class SerieAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fechaInicio', 'fechaActualizacion',)
    ordering = ('nombre',)


class AreaProcedenciaNAdmin(admin.ModelAdmin):
    list_display = ('claveAreaSIO', 'nombreAreaSIO', 'nombreArea',)
    ordering = ('nombreAreaSIO',)


class EstatusExpedienteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)


class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ('clave', 'folioSIO', 'idUsuarioCreador', 'idInstitucion', 'reclamante',
                    'idTipoMacroproceso', 'idMacroproceso', 'fechaCreacion', 'idEstatus', )
    ordering = ('-fechaCreacion',)
    search_fields = ('clave', 'idUsuarioCreador__username', 'folioSIO')

    # AUTOCOMPLETADO DE ÁREAS PARA FACILITAR ENCONTRARLAS
    autocomplete_fields = ['idInstitucion']
    # DEBE ESTAR EL SEARCH_FIELDS ACTIVADO EN EL ADMIN DE
    # LAS INSTITUCIONES FINANCIERAS
    # PARA EL AUTOCOMPLETADO


class ExpedienteOptionsAdmin(admin.ModelAdmin):
    list_display = ('idArea', 'idTipoMacroproceso', 'idProceso', 'idSerie', )
    ordering = ('idArea',)


admin.site.site_header = "CONDUSEF-Gestor de documentación digital"
admin.site.register(InstitucionesFinancieras, InstitucionesFinancierasAdmin)
admin.site.register(TipoDocumental, TipoDocumentalAdmin)
admin.site.register(EstatusCatalogo, EstatusCatalogoAdmin)
admin.site.register(TipoMacroproceso, TipoMacroprocesoAdmin)
admin.site.register(Macroproceso, MacroprocesoAdmin)
admin.site.register(Proceso, ProcesoAdmin)
admin.site.register(TipoOrdenamiento, TipoOrdenamientoAdmin)
admin.site.register(Areas, AreasAdmin)
admin.site.register(AreaSIO, AreaSIOAdmin)
admin.site.register(Serie, SerieAdmin)
admin.site.register(AreaProcedenciaN, AreaProcedenciaNAdmin)
admin.site.register(EstatusExpediente, EstatusExpedienteAdmin)
admin.site.register(Expediente, ExpedienteAdmin)
admin.site.register(ExpedienteOptions, ExpedienteOptionsAdmin)
