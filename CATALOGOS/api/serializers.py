from dataclasses import fields
from rest_framework import serializers
from CATALOGOS.models import EstatusCatalogo,TipoDocumental ,TipoMacroproceso, Macroproceso, Proceso, TipoOrdenamiento, AreaSIO, Serie,Areas ,AreaProcedenciaN, EstatusExpediente, Expediente, InstitucionesFinancieras, ExpedienteOptions


class InstitucionesFianancierasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InstitucionesFinancieras
        fields = '__all__'


class EstatusCatalogoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EstatusCatalogo
        fields = '__all__'


class TipoDocumentalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoDocumental
        fields = '__all__'
        

class TipoMacroprocesoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoMacroproceso
        fields = '__all__'
        

class MacroprocesoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Macroproceso
        fields = '__all__'
        

class ProcesoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Proceso
        fields = '__all__'
        

class TipoOrdenamientoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TipoOrdenamiento
        fields = '__all__'
        

class AreaSIOSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AreaSIO
        fields = '__all__'
        

class SerieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Serie
        fields = '__all__'
        

class AreaProcedenciaNSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AreaProcedenciaN
        fields = '__all__'
        

class AreasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Areas
        fields = '__all__'
        

class EstatusExpedienteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EstatusExpediente
        fields = '__all__'
        

class ExpedienteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Expediente
        fields = '__all__'
        

class ExpedienteOptionsSerializer(serializers.ModelSerializer):
    
    idArea = AreasSerializer(read_only=True) #CON "read_only", VEMOS TODOS LOS DATOS, PERO VAMOS A NECESITAR objects.create() PARA AGREGAR ESTOS CAMPOS
    idTipoMacroproceso = TipoMacroprocesoSerializer(read_only=True)
    idMacroproceso = MacroprocesoSerializer(read_only=True)
    idProceso = ProcesoSerializer(read_only=True)
    idSerie = SerieSerializer(read_only=True)
    
    class Meta:
        model = ExpedienteOptions
        fields = '__all__'