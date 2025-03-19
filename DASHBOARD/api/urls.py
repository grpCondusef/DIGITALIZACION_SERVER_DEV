from django.urls import path
from DASHBOARD.api.views import GetEachFileWithTheirNumberOfLoadedPages, GetExpedientesWithoutByAreaDocuments, GetEachFileWithTheirNumberOfLoadedPages, \
PercentageOfDigitizedDocumentsPieView, GetPercentageOfDigitizedDocumentsByUAUView, GetPercentageOfDigitizedDocumentsByMonthView, \
GetDeletedDocumentsByUAUView, GetUploadedPDFSByUAU, GetCreatedExpedientesByUAU, GetDeletedExpedientesByUAU, GetEmptyExpedientesBySelectedArea

urlpatterns = [
    path('percentage-digitizacion-documents-pie/', PercentageOfDigitizedDocumentsPieView.as_view(), name='percentage-digitizacion-documents-pie'),
    path('get-expedientes-without-documents-by-area/', GetExpedientesWithoutByAreaDocuments.as_view(), name='get-expedientes-without-documents-by-area'),
    path('get-percentage-of-digitized-documents-by-uau/', GetPercentageOfDigitizedDocumentsByUAUView.as_view(), name='get-percentage-of-digitized-documents-by-uau'),
    path('get-percentage-of-digitized-documents-by-month/', GetPercentageOfDigitizedDocumentsByMonthView.as_view(), name='get-percentage-of-digitized-documents-by-month'),
    path('get-each-file-with-their-number-of-loaded-pages/', GetEachFileWithTheirNumberOfLoadedPages.as_view(), name='get-each-file-with-their-number-of-loaded-pages'),
    path('get-deleted-documents/', GetDeletedDocumentsByUAUView.as_view(), name='get-deleted-documents'),
    path('get-uploaded-pdfs/', GetUploadedPDFSByUAU.as_view(), name='get-uploaded-pdfs'),
    path('get-created-expedientes/', GetCreatedExpedientesByUAU.as_view(), name='get-created-expedientes'),
    path('get-deleted-expedientes/', GetDeletedExpedientesByUAU.as_view(), name='get-deleted-expedientes'),
    path('get-empty-expedientes-by-selected-area/', GetEmptyExpedientesBySelectedArea.as_view(), name='get-empty-expedientes-by-selected-area'),
]