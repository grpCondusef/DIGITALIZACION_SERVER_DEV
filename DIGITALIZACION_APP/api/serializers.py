from rest_framework import serializers
from DIGITALIZACION_APP.models import OriginalDocuments, SplitDocuments
from CATALOGOS.api.serializers import TipoDocumentalSerializer, ExpedienteSerializer


class DocumentsSerializer(serializers.ModelSerializer):
    
    tipo = TipoDocumentalSerializer(read_only=True)
    expediente = ExpedienteSerializer(read_only=True)
    
    class Meta:
        model = OriginalDocuments
        fields = '__all__'


class SplitDocumentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SplitDocuments
        fields = '__all__'