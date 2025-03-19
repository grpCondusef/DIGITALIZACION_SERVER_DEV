from django.urls import path
from CATALOGOS.api.views import ExpedientesListView,ExpedienteInfoView,EliminarExpedienteSistemaView,\
IFListView, AddExpedientesView, \
TipoMacroprocesoOptionsView, MacroprocesoOptionsView, ProcesoOptionsView, SerieOptionsView,\
ExpedientesSearch, ConsultaMasivaView, CargaMasivaView

urlpatterns = [
    path('tipomacroproceso-options-view/', TipoMacroprocesoOptionsView.as_view(), name='tipomacroproceso-options-view'),
    path('if-lista-view/', IFListView.as_view(), name='if-lista-view'),
    path('expedientes-lista-view/', ExpedientesListView.as_view(), name='expedientes-lista-view'),
    path('carga-masiva-expedientes/', CargaMasivaView.as_view(), name='carga-masiva-expedientes'),
    path('expediente-add-view/', AddExpedientesView.as_view(), name='expediente-add-view'),
    path('expediente-info/<int:id>', ExpedienteInfoView.as_view(), name='expediente-info'),
    path('expediente-system-remove/<int:id>', EliminarExpedienteSistemaView.as_view(), name='expediente-system-remove'),
    path('expedientes-search/', ExpedientesSearch.as_view(), name='registros-search'),
    path('consulta-masiva/', ConsultaMasivaView.as_view(), name='consulta-masiva'),
    path('macroproceso-options-view/', MacroprocesoOptionsView.as_view(), name='macroproceso-options-view'),
    path('proceso-options-view/', ProcesoOptionsView.as_view(), name='proceso-options-view'),
    path('serie-options-view/', SerieOptionsView.as_view(), name='serie-options-view'),
]
