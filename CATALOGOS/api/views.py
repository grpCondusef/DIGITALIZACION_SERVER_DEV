from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict #PARA LEER TABLAS INTERMEDIAS
from rest_framework import status, generics #PARA MANDAR EL ESTATUS DEL REQUEST, VISTAS GENÉRICAS Y BÚSQUEDAS
from django.db.models import Q
from datetime import datetime
import pandas as pd
import os
from pathlib import Path
import pytz #PARA TRABAJAR CON LA FECHA
from django.forms.models import model_to_dict
from CATALOGOS.models import Areas, AreaSIO, TipoDocumental, TipoMacroproceso, Macroproceso, Proceso, Serie, Areas, Expediente, InstitucionesFinancieras, ExpedienteOptions, AlfrescoCCA, SerieVigenciaDocumental, SerieValoracionPrimaria
from CATALOGOS.api.serializers import TipoDocumentalSerializer,TipoMacroprocesoSerializer, MacroprocesoSerializer, ProcesoSerializer, SerieSerializer, ExpedienteSerializer, InstitucionesFianancierasSerializer
from rest_framework.permissions import IsAuthenticated #PARA RESTRINGIR EL ACCESO A USUARIOS AUTENTICADOS
from USER_APP.api.permissions import CrearExpedientesPermission, CargaMasivaPermission, RemoveExpedientesPermission
from CATALOGOS.api.pagination import Pagination
from USER_APP.models import User
from CATALOGOS.api.functions.generarConsecutivo import generarConsecutivo
from CATALOGOS.api.functions.transformFolioSio import transformFolioSio
from DIGITALIZACION_APP.models import Portadas
from DIGITALIZACION_APP.api.helpers.crearPortada import crear_portada
from django.core.cache import cache
from django.utils import timezone

BASE_DIR = Path(__file__).resolve().parent.parent.parent
    

class TipoMacroprocesoOptionsView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def get(self, request):
        
        data = {}
        
        user = self.request.user
        
        # OBTENER LOS id´s DE LOS PARÁMETROS DEL ENDPOINT
        idArea_id = self.request.query_params.get("area_id")
        
        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if not request.auth:
            data['error'] = "Es necesario proporcionar el token de acceso."
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # VERIFICAR QUE SE PROPORCIONÓ EL ÁREA
        if idArea_id is None:
            return Response({'error': 'El id del área no fue proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        idArea_id = int(idArea_id)
        
        try:
            expediente_options = ExpedienteOptions.objects.filter(idArea=idArea_id)
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar los tipos de macroproceso disponbles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
        if expediente_options.exists(): 
        
            tipo_macroprocesos_array = []
            id_tipo_macroprocesos_set = set()  # Utilizamos un conjunto para garantizar unicidad
            for option in expediente_options:
                tipo_macroproceso_id = option.idTipoMacroproceso.id
                
                if tipo_macroproceso_id not in id_tipo_macroprocesos_set:
                    tipo_macroproceso_item = {
                        'tipo_macroproceso_id': tipo_macroproceso_id,
                        'tipo_macroproceso_nombre': option.idTipoMacroproceso.nombre
                    }
                    tipo_macroprocesos_array.append(tipo_macroproceso_item)
                    id_tipo_macroprocesos_set.add(tipo_macroproceso_id)
                
            return Response({'area': user.area.id, 'tipo_macroproceso': tipo_macroprocesos_array}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen registros para esta consulta'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class MacroprocesoOptionsView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS

    def get(self, request):
        
        data = {}
        
        # OBTENER LOS id´s DE LOS PARÁMETROS DEL ENDPOINT
        idTipoMacroproceso_id = self.request.query_params.get("tipomacroproceso_id", None)
        idArea_id = self.request.query_params.get("area_id", None)
                
        
        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if not request.auth:
            data['error'] = "Es necesario proporcionar el token de acceso."
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        required_fields = ['tipomacroproceso_id', 'area_id']
        
        # DEVUELVE EL "campo obligatorio" SI NO VIENE EN "expediente_data" Y ES UNA LISTA
        missing_fields = [field for field in required_fields if field not in request.query_params]
        
        # SI HAY DATOS EN "missing_fields" 
        if missing_fields:
            data['error'] = f'Es necesario proporcionar: {", ".join(missing_fields)}'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # Convertir a entero
        idTipoMacroproceso_id = int(idTipoMacroproceso_id)
        idArea_id = int(idArea_id)

        try:
            # Obtener opciones de expediente filtradas
            expediente_options = ExpedienteOptions.objects.filter(idArea_id=idArea_id, idTipoMacroproceso_id=idTipoMacroproceso_id)

        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar los macroprocesos disponbles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
        if expediente_options.exists():
            # Obtener macroprocesos únicos
            macroprocesos_dict = {}
            for option in expediente_options:
                macroproceso_id = option.idMacroproceso.id
                if macroproceso_id not in macroprocesos_dict:
                    macroprocesos_dict[macroproceso_id] = {
                        'macroproceso_id': macroproceso_id,
                        'macroproceso_nombre': option.idMacroproceso.nombre
                    }

            # Convertir el diccionario a una lista 
            macroprocesos_array = list(macroprocesos_dict.values())

            return Response({
                'macroprocesos': macroprocesos_array,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen registros para esta consulta'}, status=status.HTTP_400_BAD_REQUEST)
    


class ProcesoOptionsView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def get(self, request):
        
        data = {}
        
        # Obtener parámetros del endpoint
        idTipoMacroproceso_id = request.query_params.get('tipomacroproceso_id')
        idMacroproceso_id = request.query_params.get('macroproceso_id')
        idArea_id = request.query_params.get('area_id')
        
        # Verificar campos obligatorios
        if None in [idTipoMacroproceso_id, idMacroproceso_id, idArea_id]:
            return Response({'error': 'Es necesario proporcionar el id del tipo de macroproceso, del macroproceso y del área'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que los campos tengan valores válidos para un ID
        if not all(val.isdigit() for val in [idTipoMacroproceso_id, idMacroproceso_id, idArea_id]):
            return Response({'error': 'Verifica que todos los valores de los campos sean válidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convertir a entero
        idTipoMacroproceso_id = int(idTipoMacroproceso_id)
        idMacroproceso_id = int(idMacroproceso_id)
        idArea_id = int(idArea_id)
        
        # Filtrar expediente options
        try:
            expediente_options = ExpedienteOptions.objects.filter(
                idArea=idArea_id,
                idTipoMacroproceso_id=idTipoMacroproceso_id,
                idMacroproceso_id=idMacroproceso_id
            )
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar los procesos disponbles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        if expediente_options.exists():
            procesos_array = []
            id_procesos_array = set()  # Utilizamos un conjunto para evitar duplicados
            
            for proceso_option in expediente_options:
                if proceso_option.idProceso.id not in id_procesos_array:
                    proceso_item = {
                        'proceso_id': proceso_option.idProceso.id,
                        'proceso_nombre': proceso_option.idProceso.nombre
                    }
                    procesos_array.append(proceso_item)
                    id_procesos_array.add(proceso_option.idProceso.id)
            
            return Response({'procesos': procesos_array}, status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen registros para esta consulta'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class SerieOptionsView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    # ----------OBTENER TODOS LOS REGISTROS DE LA BASE DE DATOS------------------------
    def get(self, request):
        
        data = {}
        
        idTipoMacroproceso_id = self.request.query_params.get('tipomacroproceso_id', None)
        idMacroproceso_id = self.request.query_params.get('macroproceso_id', None)
        idProceso_id = self.request.query_params.get('proceso_id', None)
        idArea_id = self.request.query_params.get("area_id", None)
        
        # Verificar campos obligatorios
        if None in [idArea_id, idTipoMacroproceso_id, idMacroproceso_id, idProceso_id]:
            return Response({'error': 'Es necesario proporcionar el id del tipo de macroproceso, del macroproceso, del proceso y del área'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convertir a entero
        idTipoMacroproceso_id = int(idTipoMacroproceso_id)
        idMacroproceso_id = int(idMacroproceso_id)
        idProceso_id = int(idProceso_id)
        idArea_id = int(idArea_id)
        
        # Filtrar expediente options
        try:
            add_options_expediente = ExpedienteOptions.objects.filter(idArea=idArea_id, idTipoMacroproceso_id=idTipoMacroproceso_id,idMacroproceso_id=idMacroproceso_id,idProceso_id=idProceso_id)
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar las series disponbles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        if add_options_expediente.exists():
            id_serie_array = []
            serie_array = []
            for serie_option in add_options_expediente:
                
                serie_item = {}
                
                if serie_option.idSerie.id not in id_serie_array:
        
                    serie_item['serie_id'] = serie_option.idSerie.id 
                    serie_item['serie_nombre'] = serie_option.idSerie.nombre 
                    serie_array.append(serie_item)
                    id_serie_array.append(serie_option.idSerie.id )
                
            return Response({
                'series': serie_array
            }, status.HTTP_200_OK)
        else:
            return Response({'error': 'No existen registros para esta consulta'}, status=status.HTTP_400_BAD_REQUEST)
        
        

# En CATALOGOS/api/views.py
class IFListView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def get(self, request):
        
        data = {}
        
        # Obtener el área del usuario
        user_area_id = self.request.user.area_id
        
        # Áreas que pueden ver opciones genéricas (ajusta según tus necesidades)
        areas_con_opciones_genericas = [1, 2, 3]  # Ejemplo: áreas 1, 2 y 3
        
        # Serie ID si se proporciona (útil si quieres filtrar por serie)
        serie_id = self.request.query_params.get('serie_id')
        
        try:    
            # Primero obtenemos las instituciones financieras regulares
            instituciones_financieras = InstitucionesFinancieras.objects.filter(
                ~Q(clave_registro__startswith='GEN_')
            ).order_by('denominacion_social')
            
            # Verificamos si el usuario tiene acceso a opciones genéricas
            if user_area_id in areas_con_opciones_genericas:
                # Obtenemos las instituciones genéricas
                instituciones_genericas = InstitucionesFinancieras.objects.filter(
                    clave_registro__startswith='GEN_'
                ).order_by('denominacion_social')
                
                # Convertimos QuerySets a listas para poder combinarlas
                todas_instituciones = list(instituciones_genericas) + list(instituciones_financieras)
            else:
                todas_instituciones = instituciones_financieras
                
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar las instituciones financieras disponibles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        instituciones_financieras_array = []
        for institucion_financiera in todas_instituciones:
            item = {}
            item['institucionFinaciera_id'] = institucion_financiera.id
            item['denominacion_social'] = institucion_financiera.denominacion_social
            item['estatus'] = institucion_financiera.estatus
            
            # Agregar un flag para identificar si es una opción genérica
            item['es_generica'] = institucion_financiera.clave_registro.startswith('GEN_') if institucion_financiera.clave_registro else False
            
            instituciones_financieras_array.append(item)
            
        return Response({
                'instituciones_financieras': instituciones_financieras_array
            }, status.HTTP_200_OK)

class AddExpedientesView(APIView):
    
    permission_classes = [CrearExpedientesPermission]
    
    def post(self, request):    
        data = {}
        user_id = self.request.user.id
        user_area = self.request.user.area_id
        expediente_data = self.request.data

        if AreaSIO.objects.filter(idArea_id=user_area).exists():
            folioSIO = transformFolioSio(expediente_data['folioSIO'].strip())
        else:
            folioSIO = expediente_data['folioSIO'].strip()
            
        required_fields = [
            'idTipoMacroproceso', 'idMacroproceso', 'idProceso', 'idSerie', 'fechaCreacion',
            'fechaApertura', 'resumenContenido', 'idAreaProcedenciaN', 'folioSIO',
            'idAreaSIO', 'reclamante', 'idInstitucion', 'idEstatus', 'pori', 'instanciaProceso', 'formatoSoporte'
        ]
        missing_fields = [field for field in required_fields if field not in expediente_data]
        if missing_fields:
            data['error'] = f'Faltan los siguientes campos obligatorios: {", ".join(missing_fields)}'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        idMacroproceso = expediente_data['idMacroproceso']
        idProceso = expediente_data['idProceso']
        idSerie = expediente_data['idSerie']
        
        try:
            macroprocesos = Macroproceso.objects.get(id=idMacroproceso)
            macroproceso_clave = macroprocesos.clave
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar los macroprocesos que están disponibles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        try:
            procesos = Proceso.objects.get(id=idProceso)
            proceso_clave = procesos.clave
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar los procesos que están disponibles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        try:
            series = Serie.objects.get(id=idSerie)
            serie_clave = series.clave
        except Exception as e:
            data['error'] = "Parece que ocurrió un error al consultar las series que están disponibles"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        today = timezone.now().date()
        actual_year = today.year
        pre_cca = f'{macroproceso_clave}.{proceso_clave}.{serie_clave}.{actual_year}'
        
        expedientes = Expediente.objects.filter(idMacroproceso=idMacroproceso, idProceso=idProceso, idSerie=idSerie, clave__contains=pre_cca)
        expedientes_folioSIO = Expediente.objects.all().exclude(idEstatus_id=4)
        
        foliosSIO_array = []
        claves_archivisticas = []
        for expediente in expedientes:
            claves_archivisticas.append(expediente.clave)
        for expediente_folio in expedientes_folioSIO:
            foliosSIO_array.append(str(expediente_folio.folioSIO.strip()))
            
        consecutivo = generarConsecutivo(claves_archivisticas)
            
        if folioSIO in foliosSIO_array and AreaSIO.objects.filter(idArea_id=user_area).exists():
            return Response({'msg':'El folio SIO ya existe!!!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cca = {}
            cca['clave_archivistica'] = f'{macroproceso_clave}.{proceso_clave}.{serie_clave}.{actual_year}.{consecutivo}'
            
            new_expediente_data = {}
            new_expediente_data['clave'] = cca['clave_archivistica']
            new_expediente_data['idUsuarioCreador'] = user_id
            new_expediente_data['idTipoMacroproceso'] = expediente_data['idTipoMacroproceso']
            new_expediente_data['idMacroproceso'] = expediente_data['idMacroproceso']
            new_expediente_data['idProceso'] = expediente_data['idProceso']
            new_expediente_data['idSerie'] = expediente_data['idSerie']

            # --- CAMBIO CRÍTICO: FECHAS AWARE ---
            try:
                fechaCreacion_str = expediente_data['fechaCreacion']
                if "T" in fechaCreacion_str:
                    fechaCreacion = timezone.make_aware(datetime.fromisoformat(fechaCreacion_str))
                else:
                    fechaCreacion = timezone.make_aware(datetime.strptime(fechaCreacion_str, "%Y-%m-%d"))
            except Exception:
                fechaCreacion = timezone.now()
            new_expediente_data['fechaCreacion'] = fechaCreacion

            try:
                fechaApertura_str = expediente_data['fechaApertura']
                if "T" in fechaApertura_str:
                    fechaApertura = timezone.make_aware(datetime.fromisoformat(fechaApertura_str))
                else:
                    fechaApertura = timezone.make_aware(datetime.strptime(fechaApertura_str, "%Y-%m-%d"))
            except Exception:
                fechaApertura = timezone.now()
            new_expediente_data['fechaApertura'] = fechaApertura

            new_expediente_data['resumenContenido'] = expediente_data['resumenContenido']
            new_expediente_data['idAreaProcedenciaN'] = expediente_data['idAreaProcedenciaN']
            new_expediente_data['folioSIO'] = folioSIO
            new_expediente_data['idAreaSIO'] = expediente_data['idAreaSIO']
            new_expediente_data['reclamante'] = expediente_data['reclamante']
            new_expediente_data['idInstitucion'] = expediente_data['idInstitucion']
            new_expediente_data['idEstatus'] = expediente_data['idEstatus']
            new_expediente_data['pori'] = expediente_data['pori']
            new_expediente_data['instanciaProceso'] = expediente_data['instanciaProceso']
            new_expediente_data['formatoSoporte'] = expediente_data['formatoSoporte']
            new_expediente_data['sistema'] = 'uridec'
            
            try:
                expediente = Expediente.objects.create(
                        clave=new_expediente_data['clave'],
                        idUsuarioCreador_id=new_expediente_data['idUsuarioCreador'],
                        idTipoMacroproceso_id=new_expediente_data['idTipoMacroproceso'],
                        idMacroproceso_id=new_expediente_data['idMacroproceso'],
                        idProceso_id=new_expediente_data['idProceso'],
                        idSerie_id=new_expediente_data['idSerie'],
                        fechaCreacion=new_expediente_data['fechaCreacion'],
                        fechaApertura=new_expediente_data['fechaApertura'],
                        resumenContenido=new_expediente_data['resumenContenido'],
                        idAreaProcedenciaN_id=new_expediente_data['idAreaProcedenciaN'],
                        folioSIO=new_expediente_data['folioSIO'],
                        idAreaSIO_id=new_expediente_data['idAreaSIO'],
                        reclamante=new_expediente_data['reclamante'],
                        idInstitucion_id=new_expediente_data['idInstitucion'],
                        idEstatus_id=new_expediente_data['idEstatus'],
                        instanciaProceso=new_expediente_data['instanciaProceso'],
                        pori=new_expediente_data['pori'],
                        formatoSoporte=new_expediente_data['formatoSoporte'],
                        sistema=new_expediente_data['sistema'],
                    )
                new_expediente_data['id'] = expediente.id
            except Exception as e:
                data['error'] = "Parece que ocurrió un error al crear el expediente con folio {}".format(new_expediente_data['folioSIO'])
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
            return Response({
                'msg': 'Expediente creado existosamente',
                'expediente_data': new_expediente_data
            }, status=status.HTTP_200_OK)

   
class CargaMasivaView(APIView):
    
    permission_classes = [CargaMasivaPermission]  # PERMISOS
    
    def post(self, request):
        
        data = {}
        
        user_id = self.request.user.id
        file = request.FILES['CARGA_MASIVA_FILE']
        datos_df = pd.read_excel(file)
        expedientes_creados = []
        counter = 0

        try:
            # QUITAR TODOS LOS DUPLICADOS CON LA FUNCIÓN "set"
            id_macroprocesos = set(datos_df['idMacroproceso_id']) 
            id_procesos = set(datos_df['idProceso_id'])
            id_series = set(datos_df['idSerie_id'])

            macroprocesos = Macroproceso.objects.filter(id__in=id_macroprocesos)
            procesos = Proceso.objects.filter(id__in=id_procesos)
            series = Serie.objects.filter(id__in=id_series)

            macroprocesos_dict = {macroproceso.id: macroproceso.clave for macroproceso in macroprocesos}
            procesos_dict = {proceso.id: proceso.clave for proceso in procesos}
            series_dict = {serie.id: serie.clave for serie in series}

            expedientes_folioSIO = Expediente.objects.exclude(idEstatus_id=4)
            foliosSIO_set = set(expediente.folioSIO.strip() for expediente in expedientes_folioSIO)

            for index, row in datos_df.iterrows():
                counter += 1
                id_macroproceso = row['idMacroproceso_id']
                id_proceso = row['idProceso_id']
                id_serie = row['idSerie_id']

                macroproceso_clave = macroprocesos_dict.get(id_macroproceso)
                proceso_clave = procesos_dict.get(id_proceso)
                serie_clave = series_dict.get(id_serie)

                today = datetime.now().replace(tzinfo=pytz.UTC).date()
                actual_year = today.year
                pre_cca = f'{macroproceso_clave}.{proceso_clave}.{serie_clave}.{actual_year}'

                expedientes = Expediente.objects.filter(
                    idMacroproceso=id_macroproceso,
                    idProceso=id_proceso,
                    idSerie=id_serie,
                    clave__contains=pre_cca
                )

                claves_archivisticas = [expediente.clave for expediente in expedientes]
                consecutivo = generarConsecutivo(claves_archivisticas)
                                                    
                claves_archivisticas = [expediente.clave for expediente in expedientes]
                consecutivo = generarConsecutivo(claves_archivisticas)

                if row['folioSIO'] not in foliosSIO_set:
                    cca = f'{macroproceso_clave}.{proceso_clave}.{serie_clave}.{actual_year}.{consecutivo}'
                    new_expediente_data = {
                        'clave': cca,
                        'idUsuarioCreador': 381,
                        'fechaCreacion': row['fechaCreacion'],
                        'fechaApertura': row['fechaApertura'],
                        'resumenContenido': row['resumenContenido'],
                        'folioSIO': row['folioSIO'],
                        'pori': "",
                        'reclamante': row['reclamante'],
                        'instanciaProceso': "",
                        'idAreaProcedenciaN': row['idAreaProcedenciaN_id'],
                        'idAreaSIO': "",
                        'idEstatus': row['idEstatus_id'],
                        'idMacroproceso': id_macroproceso,
                        'idProceso': id_proceso,
                        'idSerie': id_serie,
                        'idTipoMacroproceso': row['idTipoMacroproceso_id'],
                        'idInstitucion': row['idInstitucion_id'],
                        'formatoSoporte': row['formatoSoporte'],
                        'sistema': 'uridec',
                    }

                    expediente_creado = Expediente.objects.create(
                                clave=new_expediente_data.get('clave'),
                                idUsuarioCreador_id=new_expediente_data.get('idUsuarioCreador'),
                                fechaCreacion=new_expediente_data.get('fechaCreacion'),
                                fechaApertura=new_expediente_data.get('fechaApertura'),
                                resumenContenido=new_expediente_data.get('resumenContenido'),
                                folioSIO=new_expediente_data.get('folioSIO'),
                                pori=new_expediente_data.get('pori'),
                                reclamante=new_expediente_data.get('reclamante'),
                                instanciaProceso=new_expediente_data.get('instanciaProceso'),
                                idAreaProcedenciaN_id=new_expediente_data.get('idAreaProcedenciaN'),
                                idAreaSIO_id=new_expediente_data.get('idAreaSIO'),
                                idEstatus_id=new_expediente_data.get('idEstatus'),
                                idMacroproceso_id=new_expediente_data.get('idMacroproceso'),
                                idProceso_id=new_expediente_data.get('idProceso'),
                                idSerie_id=new_expediente_data.get('idSerie'),
                                idTipoMacroproceso_id=new_expediente_data.get('idTipoMacroproceso'),
                                idInstitucion_id=new_expediente_data.get('idInstitucion'),
                                formatoSoporte=new_expediente_data.get('formatoSoporte'),
                                sistema=new_expediente_data.get('sistema'),
                                )
                    
                    expediente_serializer = ExpedienteSerializer(expediente_creado)
                
                    expedientes_creados.append(expediente_serializer.data)
                    
                    expediente_data = expediente_serializer.data

                    expediente_id = expediente_data.get('id')
                    expediente = Expediente.objects.get(id=expediente_id)
                    clave = expediente.clave
                    serie_id = expediente.idSerie.id
                    
                    # Consulta única para obtener las vigencias
                    try:
                        vigencias = SerieVigenciaDocumental.objects.filter(idSerie_id=serie_id)
                    except Exception as e:
                        data['error'] = 'Parece que ha habido un error al intentar consultar las vigencias documentales disponibles para este expediente'
                        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    # Asignación de las vigencias
                    vigencia_ids = {1: None, 2: None, 3: None}
                    for vigencia in vigencias:
                        vigencia_ids[vigencia.idVigenciaDocumental_id] = {}

                        vigencia_ids[vigencia.idVigenciaDocumental_id]["anios"] = vigencia.anios
                        vigencia_ids[vigencia.idVigenciaDocumental_id]["meses"] = vigencia.meses
                        vigencia_ids[vigencia.idVigenciaDocumental_id]["dias"] = vigencia.dias

                    # Obtener los nombres de las valoraciones primarias en un array
                    try:
                        valoresDocumentales_array = [valor.idValoracionPrimaria.nombre for valor in SerieValoracionPrimaria.objects.filter(idSerie_id=serie_id)]
                    except Exception as e:
                        data['error'] = 'Parece que hubo un error al intentar consultar los valores documentales disponibles para este expediente'
                        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                    actual_year = datetime.now().year
                    actual_month = datetime.now().month
                    actual_day = datetime.now().day
                    
                    # ESTABLECER EL PATH EN DONDE ESTÁN LAS IMÁGENES DE LA PORTADA
                    path_img = os.path.join(BASE_DIR, 'archexpedientes/img/')

                    # SI YA FUE CREADA LA PORTADA, SOLAMENTE RETORNAMOS SU PATH
                    if Portadas.objects.filter(expediente_id=expediente_id).exists():
                        try:
                            portadas = Portadas.objects.get(expediente_id=expediente_id)
                            return Response({'pdf_url': portadas.path}, status=status.HTTP_200_OK)
                        except Exception as e:
                            data['error'] = 'Parece que hubo un error obteniendo la portada asociada a este expediente desde la base de datos'
                            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:  # SINO, CREAMOS LA PORTADA
                        try:
                            Portadas.objects.create(
                                name=f'Portada del expediente {clave}',
                                path='uridec/pdf_portadas/{}/{}/{}/{}_portada.pdf'.format(actual_year, actual_month, actual_day, clave),
                                expediente_id=expediente_id,
                                user_id=user_id,
                            )
                            # CREAR EL PDF DE LA PORTADA EN EL SISTEMA
                            crear_portada(BASE_DIR, path_img, clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id)
                        except Exception as e:
                            data['error'] = 'Parece que hubo un error al intentar agregar la portada a la base de datos'
                            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
            return Response( {
                        'msg': 'Expedientes creados existosamente',
                        'expedientes_creados': expedientes_creados,
                        'total_expedientes': counter,
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


class ExpedientesListView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def get(self, request):
        
        data = {}
        
        # Verificar si los datos están en caché
        cache_key = 'expedientes_list'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # Si los datos están en caché, retornar la respuesta cacheada
            return Response(cached_data)

        size = self.request.query_params.get("size", None)
        page = self.request.query_params.get("page", None)
        user = request.user
        
        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if not request.auth:
            data['error'] = "Es necesario proporcionar el token de acceso."
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # VERIFICAR QUE VIENE EL TAMAÑO DE LA CONSULTA Y LA PÁGINA
        if size is None or page is None:
            data['error'] = 'Es necesario proporcionar el tamaño de la consulta y la página'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        size = int(size)
        page = int(page)
        expedientes_array = []

        consulta_completa = user.consulta_completa
        
        if consulta_completa:
            try:
                expedientes = Expediente.objects.filter(sistema='uridec').exclude(idEstatus_id=4).order_by('-fechaCreacion')
            except Exception as e:
                data['error'] = 'Parece que ha habido un error al intentar consultar la lista de expedientes'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                users = User.objects.filter(id=user.id)
                areas_asociadas_array = []
                for user in users:
                    areas_asociadas = user.areas_asociadas.all()
                    for area in areas_asociadas:
                        areas_asociadas_array.append(model_to_dict(area))
            except Exception as e:
                data['error'] = 'Parece que ha habido un error al intentar consultar las áreas asociadas al usuario'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            expedientes_array = []
            for area in areas_asociadas_array:
                area_id = area.get('id')
                try:
                    expedientes = Expediente.objects.filter(idAreaProcedenciaN_id=area_id, sistema='uridec').exclude(idEstatus_id=4).order_by('-fechaCreacion')
                except Exception as e:
                    data['error'] = 'Parece que ha habido un error al intentar consultar los expedientes relacionados a las áeras asociadas al usuario'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        paginacion = Pagination(expedientes, size, page)
        expedientes_paginados = paginacion.elementosDePaginaActual()
                    
        for expediente in expedientes_paginados:
            item = {}
            item['id'] = expediente.id
            item['clave'] = expediente.clave
            item['idUsuarioCreador'] = expediente.idUsuarioCreador.id
            item['idTipoMacroproceso'] = expediente.idTipoMacroproceso.id
            item['tipoMacroproceso'] = expediente.idTipoMacroproceso.nombre
            item['idMacroproceso'] = expediente.idMacroproceso.id
            item['idProceso'] = expediente.idProceso.id
            item['idSerie'] = expediente.idSerie.id
            item['idSubserie'] = expediente.idSubserie
            item['fechaCreacion'] = expediente.fechaCreacion
            item['fechaApertura'] = expediente.fechaApertura
            item['resumenContenido'] = expediente.resumenContenido
            if expediente.idAreaProcedenciaN.id != '':
                item['idAreaProcedenciaN'] = expediente.idAreaProcedenciaN.id
            item['folioSIO'] = expediente.folioSIO
            item['pori'] = expediente.pori
            item['reclamante'] = expediente.reclamante
            item['idEstatus'] = expediente.idEstatus.id
            item['estatus'] = expediente.idEstatus.nombre
            item['instanciaProceso'] = expediente.instanciaProceso

            try:
                institucion_financiera = InstitucionesFinancieras.objects.get(id=expediente.idInstitucion.id)
                item['institucion_financiera'] = institucion_financiera.denominacion_social
                item['idInstitucion'] = institucion_financiera.id
            except:
                pass

            expedientes_array.append(item)

        # Generar los datos de respuesta
        response_data = {
            'expedientes': expedientes_array,
            "total_expedientes": paginacion.totalExpedientes(),
            'total_de_paginas': paginacion.paginasTotales(),
            'paginas': paginacion.paginasList(),
            'siguiente_pagina': paginacion.siguientePagina(),
            'pagina_anterior': paginacion.paginaAnterior()
        }

        # Guardar los datos en caché
        cache.set(cache_key, response_data, timeout=30)  # Almacenar en caché, 30 segundos
        return Response(response_data, status=status.HTTP_200_OK)



class ExpedienteInfoView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    # ----------OBTENER TODOS LOS REGISTROS DE LA BASE DE DATOS------------------------
    def get(self, request, id):
        
        data = {}
        
        # OBTENER LA INFORMACIÓN DEL EXPEDIENTE SELECCIONADO
        try:
            expedientes = Expediente.objects.filter(id=id)
        except Exception as e:
            data['error'] = ''
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        for expediente in expedientes:
            item = {}
            item['id'] = expediente.id
            item['clave'] = expediente.clave
            item['idTipoMacroproceso'] = expediente.idTipoMacroproceso.nombre
            item['idMacroproceso'] = expediente.idMacroproceso.nombre
            item['idProceso'] = expediente.idProceso.nombre
            item['idSerie'] = expediente.idSerie.nombre
            item['idSubserie'] = expediente.idSubserie
            item['fechaCreacion'] = expediente.fechaCreacion
            item['fechaApertura'] = expediente.fechaApertura
            item['resumenContenido'] = expediente.resumenContenido
            item['idAreaProcedenciaN'] = expediente.idAreaProcedenciaN.nombre
            item['folioSIO'] = expediente.folioSIO
            item['pori'] = expediente.pori
            if expediente.idAreaSIO:
                item['idAreaSIO'] = expediente.idAreaSIO.nombre
            item['reclamante'] = expediente.reclamante
            if expediente.idInstitucion is not None:
                    item['idInstitucion'] = expediente.idInstitucion.id
                    item['institucion_financiera'] = expediente.idInstitucion.denominacion_social
            else: 
                item['idInstitucion'] = ''
                item['institucion_financiera'] = ''
            
            item['idEstatus'] = expediente.idEstatus.nombre
            item['instanciaProceso'] = expediente.instanciaProceso
            item['formatoSoporte'] = expediente.formatoSoporte

        return Response(item, status=status.HTTP_200_OK)
    
    

class EliminarExpedienteSistemaView(APIView):
    
    permission_classes = [RemoveExpedientesPermission]  # PERMISOS
    
    def put(self, request, id):
        
        data = {}
        
        # CAMBIAR ESTATUS DEL EXPEDIENTE SELECCIONADO
        try:
            Expediente.objects.filter(id=id).update(idEstatus=4)
            
            return Response({'success': 'El expediente se ha eliminado del sistema correctamente'},
                            status=status.HTTP_204_NO_CONTENT)
        except:
            data['error'] = 'Parece que ocurrió un error al intentar eliminar el expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
        
# VISTA PARA LA BÚSQUEDA DE REGISTROS, PERO RETORNA SOLAMENTE LOS DEL USUARIO LOGEADO
class ExpedientesSearch(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def post(self, request):
        
        data = {}
        
        user = self.request.user
        search_data = self.request.data
        size = int(self.request.query_params.get("size", None))
        page = int(self.request.query_params.get("page", None))
        
        if size is None or page is None:
            data['error'] = 'Es necesario proporcionar la cantidad de registros y la página'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        consulta_completa = user.consulta_completa
        
        if 'search' not in search_data:
            data['error'] = 'Es necesario proporcionar el campo search'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        search = search_data['search'].strip() # BORRAMOS ESPACIOS EN BANCO AL INICIO Y AL FINAL DE LA BÚSQUEDA

        try:
            expedientes = Expediente.objects.filter(
                Q(idInstitucion_id__denominacion_social__icontains=search) |
                Q(idTipoMacroproceso__nombre__contains=search) |
                Q(clave__contains=search) |
                Q(reclamante__icontains=search) |
                Q(folioSIO__contains=search) |
                Q(pori__contains=search) |
                Q(fechaCreacion__contains=search) |
                Q(fechaApertura__contains=search)
                ).exclude(idEstatus_id=4).order_by('-fechaCreacion')
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar generar la búsqueda'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        if not consulta_completa:
            areas_asociadas_array = user.areas_asociadas.values_list('id', flat=True)
            try:
                expedientes = expedientes.filter(idAreaProcedenciaN_id__in=areas_asociadas_array).exclude(idEstatus_id=4)
            except Exception as e:
                data['error'] = 'Parece que hubo un error al intentar filtrar los expedientes del área del usuario'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        resultados = expedientes.count()

        if resultados > 0:
            paginator = Pagination(expedientes, size, page)
            expedientes_paginados = paginator.elementosDePaginaActual()

            expedientes_array = []
            for expediente in expedientes_paginados:
                item = {
                    'id': expediente.id,
                    'clave': expediente.clave,
                    'idUsuarioCreador': expediente.idUsuarioCreador.id,
                    'idTipoMacroproceso': expediente.idTipoMacroproceso.nombre,
                    'idMacroproceso': expediente.idMacroproceso.id,
                    'idProceso': expediente.idProceso.id,
                    'idSerie': expediente.idSerie.id,
                    'idSubserie': expediente.idSubserie,
                    'fechaCreacion': expediente.fechaCreacion,
                    'fechaApertura': expediente.fechaApertura,
                    'resumenContenido': expediente.resumenContenido,
                    'idAreaProcedenciaN': expediente.sistema if expediente.sistema != None else '',
                    'folioSIO': expediente.folioSIO,
                    'reclamante': expediente.reclamante,
                    'idEstatus': expediente.idEstatus.id,
                    'estatus': expediente.idEstatus.nombre,
                    'instanciaProceso': expediente.instanciaProceso,
                    #'institucion_financiera': expediente.idInstitucion.denominacion_social
                }
                if expediente.idInstitucion is not None:
                    item['institucion_financiera'] = expediente.idInstitucion.denominacion_social
                else: 
                    item['institucion_financiera'] = 'N/A'

                expedientes_array.append(item)

            return Response({
                'expedientes': expedientes_array,
                "total_expedientes": resultados,
                'total_de_paginas': paginator.paginasTotales(),
                'paginas': paginator.paginasList(),
                'pagina_actual': paginator.paginaActual(),
                'siguiente_pagina': paginator.siguientePagina(),
                'pagina_anterior': paginator.paginaAnterior()
            }, status=status.HTTP_200_OK)

        else:
            return Response({'msg': 'No hay resultados para esta búsqueda'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ConsultaMasivaView(generics.ListAPIView):
        # ----------OBTENER TODOS LOS REGISTROS DE LA BASE DE DATOS------------------------
    def get(self, request):
        
        fecha_inicio='2023-01-13'
        fecha_final='2023-01-20'
        fecha_inicio = datetime.strptime(fecha_inicio,'%Y-%m-%d')
        fecha_final = datetime.strptime(fecha_final,'%Y-%m-%d')
        
        expedientes_array = []
        
        expedientes = Expediente.objects.filter(fechaCreacion__gte=fecha_inicio,fechaCreacion__lte=fecha_final , sistema='uridec').exclude(idEstatus_id=4).order_by('-fechaCreacion')
        
        for expediente in expedientes:
            item = {}
            item['id'] = expediente.id
            item['clave'] = expediente.clave
            item['fechaCreacion'] = expediente.fechaCreacion
            expedientes_array.append(item)
       
        return Response({'expedientes': expedientes_array})
        
