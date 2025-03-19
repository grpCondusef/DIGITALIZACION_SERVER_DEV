from django.urls import path
from DIGITALIZACION_APP.api.views import DocumentsListView, AddDocumentView, DeleteSelectedDocuments, VerPortada,ActualizarPortadaView, GenerarIntegrado , GenerarIntegradoConArchivosSeleccionados,TotalScannedPages, ViewDocumentFromSIOView, GetDocumentsListFromSIOView, SendDocumentSINE


urlpatterns = [
    path('add-document-view/', AddDocumentView.as_view(), name='add-document-view'),
    path('documents-lista-view/', DocumentsListView.as_view(), name='documents-view'),
    path('delete-selected-documents/', DeleteSelectedDocuments.as_view(), name='delete-selected-documents'),
    path('ver-portada/', VerPortada.as_view(), name='ver-portada'),
    path('actualizar-portada/', ActualizarPortadaView.as_view(), name='ver-portada'),
    path('generar-integrado/', GenerarIntegrado.as_view(), name='generar-integrado'),
    path('generar-integrado-con-archivos-seleccionados/', GenerarIntegradoConArchivosSeleccionados.as_view(), name='generar-integrado-con-archivos-seleccionados'),
    path('get-document-list-from-SIO/', GetDocumentsListFromSIOView.as_view(), name='get-document-list-from-SIO'),
    path('get-document-from-SIO/', ViewDocumentFromSIOView.as_view(), name='get-document-from-SIO'),
    path('total-scanned-pages/', TotalScannedPages.as_view(), name='total-scanned-pages'),
    path('send-document-sine/', SendDocumentSINE.as_view(), name='send-document-sine'),

]