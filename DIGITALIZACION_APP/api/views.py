from PyPDF2 import PdfMerger, PdfReader
import pandas as pd
from rest_framework.views import APIView
import fitz
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated #PARA RESTRINGIR EL ACCESO A USUARIOS AUTENTICADOS
from datetime import datetime, timedelta
from DIGITALIZACION_APP.models import OriginalDocuments, Portadas, SplitDocuments
from CATALOGOS.models import Expediente, TipoDocumental, SerieVigenciaDocumental, SerieValoracionPrimaria
from fpdf import FPDF
from django.http import HttpResponse
from pathlib import Path
import os
from os import remove
from USER_APP.api.permissions import SubirDocumentosPermission, DeleteDocumentsPermission
from concurrent.futures import ThreadPoolExecutor
from DIGITALIZACION_APP.api.helpers.ProcessDocuments import process_document
from DIGITALIZACION_APP.api.helpers.crearPortada import crear_portada
from DIGITALIZACION_APP.api.helpers.countePDFPages import count_pdf_pages
from DIGITALIZACION_APP.api.helpers.sendConfirmationEmail import sendConfirmationEmail
from DIGITALIZACION_APP.api.helpers.mergeFiles import merge_files
from DIGITALIZACION_APP.api.helpers.getDocumentspath import get_documents_paths
from .helpers.foliador import foliador
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class AddDocumentView(APIView):

    permission_classes = [SubirDocumentosPermission]  # PERMISOS

    # ----------CREAR NUEVO REGISTRO------------------------
    def post(self, request):
        
        data = {}
        
        request_data = self.request.data
        user_id = self.request.user.id
        username = self.request.user.username
        expediente_id = request_data.get('expediente')
        file = request_data.get('uploadedFile')
        file_name = request_data.get('title')

        # VERIFICAR QUE VIENEN TODOS LOS CAMPOS OBLIGATORIOS
        if expediente_id is None or file is None or file_name is None:
            data['error'] = "Todos los campos son obligatorios"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        expediente_id = int(expediente_id)

        # OBTENER LA CLAVE ARCHIVÍSTICA DEL EXPEDIENTE PARA USARLO EN "createNewPDF" Y "sendConfirmationEmail"
        try:
            expediente = Expediente.objects.get(id=expediente_id)
            clave_expediente = expediente.clave
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al intentar consultar la clave del expediente al que intentas agregar un documento'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # OBTENER EL TOTAL DE DOCUMENTOS CARGADOS PREVIAMENTE, PARA ASIGNARLE UN NÚMERO AL NOMBRE DEL NUEVO ARCHIVO
        try:
            total_documents = OriginalDocuments.objects.filter(expediente=expediente_id).order_by('date_creation').count() + 1
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al intentar consultar el total de documentos'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # OBTENER LOS TIPOS DOCUMENTALES DISPONIBLES EN LA BASE DE DATOS, PARA ASIGNARLOS EN LA CLASIFICACIÓN DE DOCUMENTOS
        tipos_array = list(TipoDocumental.objects.values_list('clave', flat=True))
            
        # CREAR EL NOMBRE DEL DOCUMENTO PARA ASIGNARLO EN LA BD    
        document_new_title = '{}_{}.pdf'.format(file_name.replace('.pdf', ""), total_documents)
        
        # AGREGAR LOS METADATOS DEL ARCHIVO A LA BD
        try:
            uploaded_file = OriginalDocuments.objects.create(
                title=document_new_title,
                uploadedFile=file,
                expediente_id=expediente_id,
                user_id=user_id
            )
            
            # EXTRAER EL NOMBRE DEL ARCHIO Y LA RUTA EN LA QUE SE ALMACENÓ, PARA UTILIZARLO EN LA CLASIFICACIÓN DE CADA SEPARADOR
            document_path = uploaded_file.uploadedFile.path
            document_name = uploaded_file.uploadedFile.name
            pdf_document = os.path.join(document_path)
            
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al itentar agregar un documento a la base de datos'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # CLASIFICAR CADA SECCIÓN DEL ARCHIVO CARGADO
        respuesta = process_document( pdf_document, tipos_array, clave_expediente, expediente_id, user_id)
        
        # SI LA CLASIFICACIÓN DE CADA SECCIÓN DEL ARCHIVO FUE EXITOSA, LO NOTIFICAMOS POR SISTEMA Y POR EMAIL
        if respuesta['msg'] == 'Separación de pdf´s concluida':
            
            sendConfirmationEmail(respuesta, username, file, clave_expediente, expediente_id)
        
            return Response({
                'msg': f'Documento agregado exitosamente!!',
                'document': document_name
                }, status=status.HTTP_200_OK)
        else:
            data['error'] = 'Parece que ha ocurrido un error al itentar procesar el documento'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class DocumentsListView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS

    # ----------OBTENER TODOS LOS REGISTROS DE LA BASE DE DATOS------------------------
    def get(self, request):

        data = {}

        expediente_id = self.request.query_params.get("expediente_id")
        
        # VERIFICAR QUE SE PROVEYÓ EL "id" DEL EXPEDIENTE
        if expediente_id is None:
            data['error'] = "Es necesario proporcionar el id del expediente"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            documents = SplitDocuments.objects.filter(expediente=expediente_id).exclude(visible=False).order_by('date_creation')
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al itentar obtener los documentos de este expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            expediente = Expediente.objects.get(id=expediente_id)
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al itentar obtener los datos del expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        clave = expediente.clave
        total_pages = 0
        document_data = []
            
        try:
            for document in documents:
                item = {} 
                item['document_id'] = document.id
                item['name'] = document.name
                item['uploadedFile'] = document.path
                item['date_creation'] = document.date_creation
                item['user'] = document.user.username
                item['tipo'] = document.tipo.nombre
                item['visible'] = document.visible
                item['expediente'] = document.expediente.id
                    
                document = os.path.join(BASE_DIR, f'archexpedientes{document.path}')
                
                # Verificar si el archivo existe
                if os.path.exists(document):
                    total_pages = count_pdf_pages(document)
                    item['total_pages'] = total_pages
                else:
                    total_pages += 0
                    item['total_pages'] = 0
                
                document_data.append(item)
                    
            return Response({
                'total_pages': total_pages,
                'documents': document_data,
                'CCA': clave
            }, status=status.HTTP_200_OK)
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar agregar los datos de los documentos del expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteSelectedDocuments(APIView):
    
    permission_classes = [DeleteDocumentsPermission]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def put(self, request):
        
        data = {}
        # TRAER "selected_documents" DESDE EL BODY DE LA REQUEST
        selected_documents = request.data.get('selected_documents')
        
        # VERIFICAR QUE FUERON PROPORCIONADOS LOS DOCUMENTOS PARA ELIMINAR
        if selected_documents is None:
            data['error'] = "No fueron proporcionados los documentos para eliminar"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # VERIFICAR QUE NO VIENE VACÍO EL ARREGLO DE DOCUMENTOS PARA ELIMINAR SELECCIONADOS
        if len(selected_documents) < 1:
            data['error'] = 'Es necesario proporcionar al menos un documento para eliminar'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            # OBTENER LOS DOCUMENTOS SELECCIONADOS DESDE LA BD Y ELIMINARLOS POR SISTEMA
            documents = SplitDocuments.objects.filter(id__in=selected_documents).values('name', 'path', 'visible')
            documents.update(visible=False)
            
            return Response({
                'msg': 'Los documentos seleccionados se han eliminado con éxito!!!',
                'documentos_eliminados': documents
            }, status=status.HTTP_200_OK)
        except:
            data['error'] = 'Parece que ha ocurrido un error al intentar eliminar los documentos seleccionados'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class GenerarIntegrado(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        data = {}

        user_id = self.request.user.id
        clave = request.data.get('clave')
        expediente_id = request.data.get('expediente')
        
        documents_array = []
        
        # CORROBORAR QUE SE PROPORCIONÓ LA CLAVE Y EL I DEL EXPEDIENTE
        if clave is None or expediente_id is None:
            data['error'] = 'Es necesario proporcionar el id y la clave del expediente'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # OBTENER LOS DOCUMENTOS DEL EXPEDIENTE
        try:
            documentos = SplitDocuments.objects.filter(expediente_id=expediente_id, visible=True).order_by('date_creation')
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al intentar obtener los datos del expediente seleccionado'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # SI EL DOCUMENTO TIENE DOCUMENTOS CARGADOS
        if documentos.count() > 0:
            
            # CONSULTADOS SI EXISTE UNA PORTADA PARA ESTE EXPEDIENTE
            try:
                portada = Portadas.objects.filter(expediente_id=expediente_id).first()
            except Exception as e:
                data['error'] = 'Parece que ha ocurrido un error al intentar consultar la portada del expediente'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # SI NO HA SIDO CREADA LA PORTADA, LA CREAMOS Y AGREGAMOS AL INTEGRADO DEL EXPEDIENTE
            if portada is None:
                
                # CONSULTAR LOS DATOS DEL EXPEDIENTE, PARA SABER QUÉ SERIE TIENE LIGADA Y AGREGAR LAS VIGENCIAS  Y VALORES 
                # DOCUMENTALES, CORRESPONDIENTES AL EXPEDIENTE
                try:
                    expediente = Expediente.objects.get(id=expediente_id)
                except Exception as e:
                    data['error'] = 'Parece que ha ocurrido un error al intentar obtener los datos del expediente'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
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

                # CREAR EL ARRAY DE LOS VALORES DOCUMENTALES RELACIONADOS CON LA SERIE DEL EXPEDIENTE
                try:
                    valoresDocumentales_array = [valor.idValoracionPrimaria.nombre for valor in SerieValoracionPrimaria.objects.filter(idSerie_id=serie_id)]
                except Exception as e:
                    data['error'] = 'Parace que hubo un error al intentar consultar los valores documentales'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                actual_year = datetime.now().year
                actual_month = datetime.now().month
                actual_day = datetime.now().day

                # ESTABLECER EL PATH EN DONDE ESTÁN LAS IMÁGENES DE LA PORTADA Y DONDE VA A CAER LA PORTADA
                path_img = os.path.join(BASE_DIR, 'archexpedientes/img/')
                portada_path = f'uridec/pdf_portadas/{actual_year}/{actual_month}/{actual_day}/{clave}_portada.pdf'
                
                try:
                    Portadas.objects.create(
                            name=f'Portada del expediente {clave}',
                            path=portada_path,
                            expediente_id=expediente_id,
                            user_id=user_id,
                        )
                except Exception as e:
                    data['error'] = 'Parece que ha habido un error al intentar crear la portada del expediente a la base de datos'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # CREAR EL PDF DE LA PORTADA
                crear_portada(BASE_DIR, path_img, clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id)
                documents_array.append(os.path.join(BASE_DIR, f'archexpedientes/{portada_path}'))
                
            else:
                documents_array.append(os.path.join(BASE_DIR, f'archexpedientes/{str(portada.path)}'))

            # OBTENER LOS PATHS DE LOS DOCUMENTOS DEL EXPEDIENTE
            get_documents_paths(BASE_DIR, documentos, documents_array)

            ubicacion_salida = os.path.join(BASE_DIR, f'archexpedientes/pdf_integrados/{clave}documento_integrado.pdf')

            # Utilizar ThreadPoolExecutor para procesar los archivos en paralelo y unirlos
            with ThreadPoolExecutor() as executor:
                executor.submit(merge_files, documents_array, ubicacion_salida)

            return Response({'documento': f'pdf_integrados/{clave}documento_integrado.pdf'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Parece que el expediente seleccionado no tiene archivos cargados'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
            


class GenerarIntegradoConArchivosSeleccionados(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = self.request.data

        user_id = self.request.user.id
        clave = data['clave']
        expediente_id = data['expediente']
        selected_documents = data['documents']
        
        documents_array = []
        
        # CORROBORAR QUE SE PROPORCIONÓ LA CLAVE Y EL I DEL EXPEDIENTE
        if clave is None or expediente_id is None:
            data['error'] = 'Es necesario proporcionar el id y la clave del expediente'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # OBTENER LOS DOCUMENTOS DEL EXPEDIENTE
        try:
            documentos = SplitDocuments.objects.filter(id__in=selected_documents, visible=True).order_by('date_creation')
        except Exception as e:
            data['error'] = 'Parece que ha ocurrido un error al intentar obtener los datos del expediente seleccionado'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # SI EL DOCUMENTO TIENE DOCUMENTOS CARGADOS
        if documentos.count() > 0:
            
            # CONSULTADOS SI EXISTE UNA PORTADA PARA ESTE EXPEDIENTE
            try:
                portada = Portadas.objects.filter(expediente_id=expediente_id).first()
            except Exception as e:
                data['error'] = 'Parece que ha ocurrido un error al intentar consultar la portada del expediente'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # SI NO HA SIDO CREADA LA PORTADA, LA CREAMOS Y AGREGAMOS AL INTEGRADO DEL EXPEDIENTE
            if portada is None:
                
                # CONSULTAR LOS DATOS DEL EXPEDIENTE, PARA SABER QUÉ SERIE TIENE LIGADA Y AGREGAR LAS VIGENCIAS  Y VALORES 
                # DOCUMENTALES, CORRESPONDIENTES AL EXPEDIENTE
                try:
                    expediente = Expediente.objects.get(id=expediente_id)
                except Exception as e:
                    data['error'] = 'Parece que ha ocurrido un error al intentar obtener los datos del expediente'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
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
                # CREAR EL ARRAY DE LOS VALORES DOCUMENTALES RELACIONADOS CON LA SERIE DEL EXPEDIENTE
                try:
                    valoresDocumentales_array = [valor.idValoracionPrimaria.nombre for valor in SerieValoracionPrimaria.objects.filter(idSerie_id=serie_id)]
                except Exception as e:
                    data['error'] = 'Parace que hubo un error al intentar consultar los valores documentales'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                actual_year = datetime.now().year
                actual_month = datetime.now().month
                actual_day = datetime.now().day

                # ESTABLECER EL PATH EN DONDE ESTÁN LAS IMÁGENES DE LA PORTADA Y DONDE VA A CAER LA PORTADA
                path_img = os.path.join(BASE_DIR, 'archexpedientes/img/')
                portada_path = f'uridec/pdf_portadas/{actual_year}/{actual_month}/{actual_day}/{clave}_portada.pdf'
                
                try:
                    Portadas.objects.create(
                            name=f'Portada del expediente {clave}',
                            path=portada_path,
                            expediente_id=expediente_id,
                            user_id=user_id,
                        )
                except Exception as e:
                    data['error'] = 'Parece que ha habido un error al intentar crear la portada del expediente a la base de datos'
                    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # CREAR EL PDF DE LA PORTADA
                crear_portada(BASE_DIR, path_img, clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id)
                documents_array.append(os.path.join(BASE_DIR, f'archexpedientes/{portada_path}'))
                
            else:
                documents_array.append(os.path.join(BASE_DIR, f'archexpedientes/{str(portada.path)}'))

            # OBTENER LOS PATHS DE LOS DOCUMENTOS DEL EXPEDIENTE
            get_documents_paths(BASE_DIR, documentos, documents_array)
            
            ubicacion_salida = os.path.join(BASE_DIR, f'archexpedientes/pdf_integrados/{clave}documento_integrado_no_foliado.pdf')

            # Utilizar ThreadPoolExecutor para procesar los archivos en paralelo y unirlos
            with ThreadPoolExecutor() as executor:
                executor.submit(merge_files, documents_array, ubicacion_salida)
                
            foliador(ubicacion_salida, os.path.join(BASE_DIR, f'archexpedientes/pdf_integrados/{clave}documento_integrado.pdf'), portada)
            
            os.remove(ubicacion_salida)

            return Response({'documento': f'pdf_integrados/{clave}documento_integrado.pdf'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Parece que el expediente seleccionado no tiene archivos cargados'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)        



class VerPortada(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS

    # ----------CREAR PORTADA------------------------
    def post(self, request):
        data = {}

        user_id = self.request.user.id
        expediente_id = request.data.get('expediente_id')
        
        # COMPROBAR QUE EL "id" DEL EXPEDIENTE FUE PROPORCIONADO
        if expediente_id is None:
            data['error'] = 'No fue proporcionado el id del expediente'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # OBETENER LOS DATOS DEL EXPEDIENTE
        try:
            expediente = Expediente.objects.get(id=expediente_id)
        except Exception as e:
            data['error'] = 'Parece que hubo un problema obteniendo los datos del expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
            except Exception as e:
                data['error'] = 'Parece que hubo un error al intentar agregar la portada a la base de datos'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # CREAR EL PDF DE LA PORTADA EN EL SISTEMA
            crear_portada(BASE_DIR, path_img, clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id)
            return Response({'pdf_url': 'uridec/pdf_portadas/{}/{}/{}/{}_portada.pdf'.format(actual_year, actual_month, actual_day, clave)}, status=status.HTTP_200_OK)


        
class ActualizarPortadaView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def put(self, request):
        
        data = {}
        
        user_id = self.request.user.id
        
        # SI "EXPEDIENTE_ID" ESTÁ EN LOS PARÁMETROS DE CONSULTA, EXPEDIENTE_ID CONTENDRÁ SU VALOR; DE LO CONTRARIO, CONTENDRÁ NONE
        expediente_id = self.request.query_params.get("expediente_id", None)
        
        if expediente_id is None:
            data['error'] = 'Es necesario proporcionar el id del expediente'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # OBETENER LOS DATOS DEL EXPEDIENTE
        try:
            expediente = Expediente.objects.get(id=expediente_id)
        except Exception as e:
            data['error'] = 'Parece que hubo un problema obteniendo los datos del expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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

        # Obtener los nombres de las valoraciones primarias en un array
        try:
            valoresDocumentales_array = [valor.idValoracionPrimaria.nombre for valor in SerieValoracionPrimaria.objects.filter(idSerie_id=serie_id)]
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar consultar los valores documentales disponibles para este expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # SI YA FUE EXISTE LA PORTADA, LA ELIMINAMOS
        if Portadas.objects.filter(expediente_id=expediente_id).exists():
            try:
                portadas = Portadas.objects.get(expediente_id=expediente_id)
                portadas.delete()
                portada_document = os.path.join(BASE_DIR, f'archexpedientes/{portadas.path}')
                remove(portada_document)
            except Exception as e:
                data['error'] = 'Parece que hubo un error obteniendo la portada asociada a este expediente desde la base de datos'
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            Portadas.objects.create(
                name=f'Portada del expediente {clave}',
                path='uridec/pdf_portadas/{}/{}/{}/{}_portada.pdf'.format(actual_year, actual_month, actual_day, clave),
                expediente_id=expediente_id,
                user_id=user_id,
            )
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar agregar la portada a la base de datos'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # CREAR EL PDF DE LA PORTADA EN EL SISTEMA
        crear_portada(BASE_DIR, path_img, clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id)
        return Response({'pdf_url': 'uridec/pdf_portadas/{}/{}/{}/{}_portada.pdf'.format(actual_year, actual_month, actual_day, clave)}, status=status.HTTP_200_OK)
    
            
        
class ViewDocumentFromSIOView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def get(self, request):
        
        data = {}
        
        document_id = self.request.query_params.get("document_id", None)
        
        # OBTENER EL ID DEL DOCUMENTO
        if document_id is None:
            data['error'] = 'Es necesario proporcionar el id del documento'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        # OBTENER LOS DATOS DEL DOCUMENTO SELECCIONADO DESDE LA BASE DE DATOS
        try:
            document = SplitDocuments.objects.get(id=document_id)
        except Exception as e:
            data['error'] = 'Hubo un error al intentar consultar los datos del documento seleccionado'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            path = os.path.join(BASE_DIR, f'archexpedientes{str(document.path)}')

            document = open(path,"rb")
            response = HttpResponse(document, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=f"8.- {document_name}"'

            return response
        except Exception as e:
            data['error'] = 'Parece que hubo un error sl intentar consultar el documento solicitado'
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    


class GetDocumentsListFromSIOView(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS

    def get(self, request):
        
        data = {}
        
        folioSIO = self.request.query_params.get("folioSIO", None)
        
        # VERIFICAR QUE FUE PROPORCIONADO EL FOLIO SIO
        if folioSIO is None:
            data['error'] = 'Es necesario proporcionar el folio SIO'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # OBTENER LOS DATOS DEL EXPEDIENTE
        try:
            expediente = Expediente.objects.get(folioSIO=folioSIO)
            expediente_id = expediente.id
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar consultar los datos del expediente'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # OBTENER LOS DOCUMENTOS DEL EXPEDIENTE
        try:
            documents = SplitDocuments.objects.filter(expediente_id=expediente_id).order_by('date_creation')
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar consultar los documentos del expediente'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        try:
            # CREAR UN DICCIONARIO CON LOS DATOS
            document_data = []
            for document in documents:
                timestamp = f'{document.date_creation}'
                parsed_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
                formatted_timestamp = parsed_timestamp.strftime("%Y-%m-%d")
                item = {}
                item['document_id'] = document.id
                item['name'] = document.name
                item['uploadedFile'] = document.path
                item['fecha'] = formatted_timestamp
                item['tipo_documental'] = document.tipo.nombre
                
                document_data.append(item)
            
            return Response({
                            'documents': document_data
                            }, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'Parece que ha habido un error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 

class TotalScannedPages(APIView):
    
    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def get(self, request):
        
        data = {}

        fecha_inicio = self.request.query_params.get("fecha_inicio", None)
        fecha_final = self.request.query_params.get("fecha_final", None)
        
        fecha_inicio = datetime.strptime(fecha_inicio,'%Y-%m-%d')
        fecha_final = datetime.strptime(fecha_final,'%Y-%m-%d')
        
        fecha_inicio = fecha_inicio - timedelta(days=1)
        fecha_final = fecha_final + timedelta(days=1)
        
        split_documents_array = []
        # OBTENER LOS EXPEDIENTES DEL PERIODO SELECCIONADO
        try:
            expedientes = Expediente.objects.filter(fechaCreacion__gte=fecha_inicio,fechaCreacion__lte=fecha_final)
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar consultar los expedientes del periodo seleccionado'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        for expediente in expedientes:
            # CONSULTAR LOS DOCUMENTOS DE UN EXPEDIENTE
            try:
                split_documents = SplitDocuments.objects.filter(expediente_id=expediente.id)
            except Exception as e:
                data['error'] = 'Parece que hubo un error al intentar consultar los documentos del expediente {}'.format(expediente.clave)
            
            total_pages = 0
            
            item = {}
            item['CCA'] = expediente.clave
            item['FOLIO SIO/EXPEDIENTE'] = expediente.folioSIO
            item['RECLAMANTE'] = expediente.reclamante
            fechaApertura = f'{expediente.fechaApertura}'
            item['FEC APERTURA'] = fechaApertura[:10]
            item['INSTITUCIÓN'] = ''
            if expediente.idInstitucion is not None:
                item['INSTITUCIÓN'] = expediente.idInstitucion.denominacion_social
                
            # SI HAY DOCUMENTOS CARGADOS EN EL EXPEDIENTE, CONTAMOS EL TOTAL DE PÁGINA QUE TIENE CADA ARCHIVO
            if split_documents.exists:
        
                for split_document in split_documents:
                    
                    date = f'{split_document.date_creation}'
                    item['FEC CARGA'] = date[:10]
                    
                    document = os.path.join(BASE_DIR, f'archexpedientes/{split_document.path}')
                    
                    try:
                        with fitz.open(document) as pdf_file:
                            total_pages += pdf_file.page_count
                    except fitz.fitz.FileDataError:
                        print(f"El archivo {document} está dañado, se omitirá.")
            else:
                item['FEC CARGA'] = ''
                
            item['NUM PAGS'] = total_pages
            item['AREA'] = expediente.idAreaProcedenciaN.nombre
            split_documents_array.append(item)
        
        # Crear un DataFrame a partir de split_documents_array
        try:
            df = pd.DataFrame(split_documents_array)
            df = pd.DataFrame(df)
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar crear el archivo excel'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Guardar el DataFrame como archivo Excel
        try:
            output_path = os.path.join(BASE_DIR, 'reporte.xlsx')
            df.to_excel(output_path, index=False)
        except Exception as e:
            data['error'] = 'Parece que hubo un error al intentar guardar el archivo excel en el servidor'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Retornar el archivo Excel en la respuesta
        response = FileResponse(open(output_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reporte.xlsx"'
        
        return response


############################### ENVÍO DE DOCUMENTOS PARA SINE ###############################

class SendDocumentSINE(APIView):

    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    
    def post(self, request):

        #Variables para acceder a los datos enviados
        data = self.request.data
        user_id = self.request.user.id        
        document = data.get('document') 
        folioSIO = data.get('folioSIO')
        tipo_documental = data.get('tipo_id')
        cadena_unique_identifier = str(uuid.uuid4())

        #Creamos una tupla con los campos requeridos del request en el POST
        required_fields = ['document', 'folioSIO', 'tipo_id', 'user_id']
        
        #Devuelve el "campo obligatorio" si no se proporciona en el POST
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            missing_fields_str = ", ".join(missing_fields)
            return Response({'error': f'Faltan los siguientes campos obligatorios: {missing_fields_str}'}, status=status.HTTP_400_BAD_REQUEST)
               
        # Obtenemos la información del expediente   
        expediente = Expediente.objects.get(folioSIO=folioSIO)
        expediente_id = expediente.id 
        clave = expediente.clave        

        # Crear las carpetas si no existen
        actual_year = datetime.now().year
        actual_month = datetime.now().month
        actual_day = datetime.now().day
        directory = os.path.join(BASE_DIR, 'archexpedientes/uridec/split_documents/{}/{}/{}'.format(actual_year, actual_month, actual_day))
        os.makedirs(directory, exist_ok=True)

        #Contamos los documentos y generamos el nuevo nombre
        documents_counter = SplitDocuments.objects.filter(expediente_id=expediente_id).count()
        document_new_title = '{}_{}.pdf'.format(data['folioSIO'].replace('.pdf', ""), documents_counter)

        # Ruta completa del documento
        document_path = os.path.join(directory, f'{documents_counter}.- {tipo_documental}_{clave}_{cadena_unique_identifier}.pdf')

        #Valida que el archivo proporcionado sea PDF, lower() para no hacer distinción entre mayúsculas y minúculas, endswith() compara la terminación de la extención
        if document.name.lower().endswith('.pdf'):
            document_path = os.path.join(directory, f'{documents_counter}.- {tipo_documental}_{clave}_{cadena_unique_identifier}.pdf')

            try:
                #Guarda los documentos en el PATH especificado, escribe el contenido
                with open(os.path.join(directory, '{}.- {}_{}_{}.pdf'.format(documents_counter, tipo_documental, clave, cadena_unique_identifier)), 'wb') as f2:
                    SplitDocuments.objects.create(
                        name=document_new_title,
                        path='/uridec/split_documents/{}/{}/{}/{}.- {}_{}_{}.pdf'.format(actual_year, actual_month, actual_day, documents_counter, tipo_documental, clave, cadena_unique_identifier),
                        expediente_id=expediente_id,
                        tipo_id=tipo_documental,
                        user_id=data['user_id']
                    )
                    f2.write(document.read()) #Nos permite leer el archivo creado, sin esto solamente se crea el archivo pero no nos permite abrirlo.

            except Exception as e:
                print(e)
                return Response(
                    {'error': 'Error al guardar el documento. El campo {} es requerido.'.format(e) },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

            #Si se proporcionan los datos correctos, regresa la respuesta
            return Response({'folioSIO': folioSIO, 'tipo_id': tipo_documental,'mensaje': 'Documento procesado exitosamente.'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'El archivo proporcionado no es PDF.'}, status=status.HTTP_400_BAD_REQUEST)