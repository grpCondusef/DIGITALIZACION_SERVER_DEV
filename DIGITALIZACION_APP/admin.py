from django.contrib import admin

# Register your models here.
from .models import OriginalDocuments, SplitDocuments, Portadas, CertificacionExpediente


class OriginalDocumentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'expediente', 'user', 'date_creation',)
    ordering = ('-date_creation', )
    # VAMOS A PODER BUSCAR CON BASE EN EL TÍTULO Y CONTENIDO DE CADA PAGINA
    search_fields = ('title',  'user__username', 'expediente__clave',)


class SplitlDocumentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'expediente', 'user', 'date_creation',)
    ordering = ('-date_creation',)
    # VAMOS A PODER BUSCAR CON BASE EN EL TÍTULO Y CONTENIDO DE CADA PAGINA
    search_fields = ('name', 'expediente__clave', 'user__username',)


class PortadasAdmin(admin.ModelAdmin):
    list_display = ('name', 'expediente', 'user', 'date_creation',)
    ordering = ('-date_creation',)
    # VAMOS A PODER BUSCAR CON BASE EN EL TÍTULO Y CONTENIDO DE CADA PAGINA
    search_fields = ('name', 'expediente__clave',)

class CertificacionExpedienteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'expediente', 'folio_expediente', 'usuario', 'area', 'fecha_certificacion',
        'recurrente', 'firmado', 'notificacion_enviada'
    )
    search_fields = ('folio_expediente', 'usuario__username', 'area__nombre', 'expediente__clave', 'recurrente')
    
admin.site.register(OriginalDocuments, OriginalDocumentsAdmin)
admin.site.register(SplitDocuments, SplitlDocumentsAdmin)
admin.site.register(Portadas, PortadasAdmin)
admin.site.register(CertificacionExpediente, CertificacionExpedienteAdmin)
