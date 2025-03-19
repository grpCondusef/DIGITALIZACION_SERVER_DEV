from django.contrib import admin
#PRUEBA PROD
# Register your models here.
from .models import OriginalDocuments, SplitDocuments, Portadas


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

admin.site.register(OriginalDocuments, OriginalDocumentsAdmin)
admin.site.register(SplitDocuments, SplitlDocumentsAdmin)
admin.site.register(Portadas, PortadasAdmin)
