from django.db.models import Q
from django.db.models import Count
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
# PARA RESTRINGIR EL ACCESO A USUARIOS AUTENTICADOS
from rest_framework.permissions import IsAuthenticated
from CATALOGOS.models import Expediente, Areas, AreaSIO
from DIGITALIZACION_APP.models import OriginalDocuments, SplitDocuments



class PercentageOfDigitizedDocumentsPieView(APIView):
     def get(self, request):
         
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        if consulta_completa:
            try:
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto') 
                
                total_expedientes = Expediente.objects.all().exclude(idEstatus=4).count()
                empty_expedientes = Expediente.objects.exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).filter(
                    idAreaProcedenciaN__in=areasSio.values_list('idArea', flat=True)).count()
                pct_digitized_expedientes = round(((total_expedientes - empty_expedientes) / total_expedientes) * 100, 2)
                pct_empty_expedientes = round((empty_expedientes / total_expedientes) * 100, 2)
            
                return Response({
                    'total_expedientes': total_expedientes,
                    'pct_empty_expedientes': pct_empty_expedientes,
                    'pct_digitized_expedientes': pct_digitized_expedientes
                })
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                total_expedientes = Expediente.objects.filter(idAreaProcedenciaN__in=areasSio.values_list('idArea__id', flat=True)).exclude(idEstatus=4).count()
                
                empty_expedientes = Expediente.objects.exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).filter(
                    idAreaProcedenciaN__in=areasSio.values_list('idArea', flat=True)).count()
                
                pct_digitized_expedientes = round(((total_expedientes - empty_expedientes) / total_expedientes) * 100, 2)
                pct_empty_expedientes = round((empty_expedientes / total_expedientes) * 100, 2)

                
                return Response({
                    'total_expedientes': total_expedientes,
                    'pct_empty_expedientes': pct_empty_expedientes,
                    'pct_digitized_expedientes': pct_digitized_expedientes
                })
            
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetExpedientesWithoutByAreaDocuments(APIView):

    def get(self, request):
        
        user = self.request.user
        consulta_completa = user.consulta_completa

        array = []
        
        if consulta_completa:
            
            try:
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')

                for areaSio in areasSio:
                    item = {}
                    item['area_id'] = areaSio.idArea.id
                    item['area'] = areaSio.nombreCorto
                    item['total'] = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).values('id', 'clave', 'folioSIO', 'idAreaProcedenciaN__nombre').count()
                    array.append(item)

                return Response({
                    'expedientes_data': array
                })
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    item['area_id'] = areaSio.idArea.id
                    item['area'] = areaSio.nombreCorto
                    item['total'] = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).values('id', 'clave', 'folioSIO', 'idAreaProcedenciaN__nombre').count()
                    array.append(item)

                return Response({
                    'expedientes_data': array
                })
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
                    
        
        
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
class GetPercentageOfDigitizedDocumentsByMonthView(APIView):
    
    def get(self, request):
        
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        if consulta_completa:
            
            try:

                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')

                # Filtrar los expedientes por área de procedencia
                empty_expedientes_by_month = Expediente.objects.exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).filter(
                    idAreaProcedenciaN__in=areasSio.values_list('idArea', flat=True)).annotate(month=TruncMonth('fechaCreacion')).values('month').annotate(count=Count('id')).order_by('month')

                # Obtener el mes y año en el formato deseado
                for item in empty_expedientes_by_month:
                    item['month'] = item['month'].strftime('%Y-%m')  # Convierte a formato YYYY-MM

                result = {
                    'empty_expedientes_by_month': empty_expedientes_by_month
                }

                return Response(result)
        
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                # Filtrar los expedientes por área de procedencia
                empty_expedientes_by_month = Expediente.objects.exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).filter(
                    idAreaProcedenciaN__in=areasSio.values_list('idArea__id', flat=True)).annotate(month=TruncMonth('fechaCreacion')).values('month').annotate(count=Count('id')).order_by('month')

                # Obtener el mes y año en el formato deseado
                for item in empty_expedientes_by_month:
                    item['month'] = item['month'].strftime('%Y-%m')  # Convierte a formato YYYY-MM

                result = {
                    'empty_expedientes_by_month': empty_expedientes_by_month
                }

                return Response(result)
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GetEachFileWithTheirNumberOfLoadedPages(APIView):
    def get(self, request):
        
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        if consulta_completa:
            try:
            
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
            
                expedientes = Expediente.objects.filter(
                        #fechaCreacion__year='2023',
                        idAreaProcedenciaN__in=areasSio.values_list('idArea', flat=True)
                    ).exclude(idEstatus=4).annotate(
                        loaded_pages=Count('splitdocuments')
                    ).values(
                        'id', 'clave', 'idAreaProcedenciaN__nombre', 'folioSIO', 'reclamante', 'idInstitucion__denominacion_social','loaded_pages', 
                    ).order_by('idAreaProcedenciaN')
                
                expedientes_array = []
                for expediente in expedientes:
                    item = {
                        'clave': expediente['clave'],
                        'area': expediente['idAreaProcedenciaN__nombre'],
                        'folio': expediente['folioSIO'],
                        'reclamante': expediente['reclamante'],
                        'institucion': expediente['idInstitucion__denominacion_social'],
                                    #resultado_si_verdadero if condicion else resultado_si_falso
                        'estatus': 'CON DOCUMENTOS' if expediente['loaded_pages'] > 0 else 'SIN DOCUMENTOS',
                        'total_documents': expediente['loaded_pages'],
                    }
                
                    expedientes_array.append(item)

                return Response({'expedientesData': expedientes_array}, status=status.HTTP_200_OK)
            
            except Exception as e:
                print(e)
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                expedientes = Expediente.objects.filter(
                        #fechaCreacion__year='2023',
                        idAreaProcedenciaN__in=areasSio.values_list('idArea', flat=True)
                    ).exclude(idEstatus=4).annotate(
                        loaded_pages=Count('splitdocuments')
                    ).values(
                        'id', 'clave', 'folioSIO', 'loaded_pages', 'idAreaProcedenciaN__nombre'
                    ).order_by('idAreaProcedenciaN')
                
                expedientes_array = []
                for expediente in expedientes:
                    item = {
                        'clave': expediente['clave'],
                        'area': expediente['idAreaProcedenciaN__nombre'],
                        'folio': expediente['folioSIO'],
                                    #resultado_si_verdadero if condicion else resultado_si_falso
                        'estatus': 'CON DOCUMENTOS' if expediente['loaded_pages'] > 0 else 'SIN DOCUMENTOS',
                        'total_documents': expediente['loaded_pages'],
                    }
                
                    expedientes_array.append(item)
                return Response({'expedientesData': expedientes_array}, status=status.HTTP_200_OK)
            
            except Exception as e:
                print(e)
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class GetDeletedDocumentsByUAUView(APIView):
    
    def get(self, request):
        
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        deleted_documents = []
        
        if consulta_completa:
        
            try:
                
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    expedientes = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4)
                    item[f'{areaSio.nombreCorto}']= SplitDocuments.objects.filter(expediente__in=expedientes, visible=False).count()
                    deleted_documents.append(item)
                
                return Response({
                    'deleted_documents': deleted_documents
                })        
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    expedientes = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4)
                    item[f'{areaSio.nombreCorto}']= SplitDocuments.objects.filter(expediente__in=expedientes, visible=False).count()
                    deleted_documents.append(item)
                
                return Response({
                    'deleted_documents': deleted_documents
                })   
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        
       
class GetUploadedPDFSByUAU(APIView):
    
    def get(self, request):
        
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        uploadedpdfs = []
        
        if consulta_completa:
        
            try:
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                for areaSio in areasSio:
                    item = {}
                    expedientes = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4)
                    item[f'{areaSio.nombreCorto}'] = OriginalDocuments.objects.filter(expediente__in=expedientes).count()
                    uploadedpdfs.append(item)
                
                return Response({
                    'uploadedpdfs': uploadedpdfs
                })        
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    expedientes = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4)
                    item[f'{areaSio.nombreCorto}'] = OriginalDocuments.objects.filter(expediente__in=expedientes).count()
                    uploadedpdfs.append(item)
                
                return Response({
                    'uploadedpdfs': uploadedpdfs
                })        
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                

        
        
        
class GetPercentageOfDigitizedDocumentsByUAUView(APIView):
    
    def get(self, request):
        
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        array = []
        
        if consulta_completa:
            
            try:
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')

                for areaSio in areasSio:
                    item = {}
                    item['area'] = areaSio.nombreCorto
                    expedientes_totales = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).values('clave', 'folioSIO', 'idAreaProcedenciaN__nombre').exclude(idEstatus=4).count()
                    expedientes_sin_digitalizacion = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).values('clave', 'folioSIO', 'idAreaProcedenciaN__nombre').count()
                    item['digitalizado'] = round(((expedientes_totales - expedientes_sin_digitalizacion) / expedientes_totales) * 100, 2)
                    item['no_digitalizado'] = round(100 - item['digitalizado'], 2)
                    array.append(item)

                return Response({
                    'digitalizacion_data': array
                })
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    item['area'] = areaSio.nombreCorto
                    expedientes_totales = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4).values('clave', 'folioSIO', 'idAreaProcedenciaN__nombre').count()
                    expedientes_sin_digitalizacion = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).values('clave', 'folioSIO', 'idAreaProcedenciaN__nombre').count()
                    item['digitalizado'] = round(((expedientes_totales - expedientes_sin_digitalizacion) / expedientes_totales) * 100, 2)
                    item['no_digitalizado'] = round(100 - item['digitalizado'], 2)
                    array.append(item)

                return Response({
                    'digitalizacion_data': array
                })
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            

class GetCreatedExpedientesByUAU(APIView):
    
    def get(self, request):
    
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        array = []
        
        if consulta_completa:
            
            try:
        
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')

                for areaSio in areasSio:
                    item = {}
                    item[f'{areaSio.nombreCorto}'] = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4).count()
                    array.append(item)
                    
                return Response({
                                'created_expedientes': array
                            })
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    item[f'{areaSio.nombreCorto}'] = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id).exclude(idEstatus=4).count()
                    array.append(item)
                    
                return Response({
                                'created_expedientes': array
                            })
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            

class GetDeletedExpedientesByUAU(APIView):
    
    def get(self, request):
    
        user = self.request.user
        consulta_completa = user.consulta_completa
        
        array = []
        
        if consulta_completa:
            
            try:
        
                areasSio = AreaSIO.objects.all().exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')

                for areaSio in areasSio:
                    item = {}
                    item[f'{areaSio.nombreCorto}'] = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id, idEstatus_id=4).count()
                    array.append(item)
                    
                return Response({
                                'deleted_expedientes': array
                            })
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        else:
            
            try:
                areas_asociadas = user.areas_asociadas.all().values_list('id', flat=True)
            
                # Filtrar los objetos en AreaSIO usando los ids obtenidos y excluyendo los casos con nombreCorto None o vacío
                areasSio = AreaSIO.objects.filter(idArea_id__in=areas_asociadas).exclude(Q(nombreCorto=None) | Q(nombreCorto="")).order_by('nombreCorto')
                
                for areaSio in areasSio:
                    item = {}
                    item[f'{areaSio.nombreCorto}'] = Expediente.objects.filter(idAreaProcedenciaN_id=areaSio.idArea_id, idEstatus_id=4).count()
                    array.append(item)
                    
                return Response({
                                'deleted_expedientes': array
                            })
                
            except Exception as e:
                return Response({'message': 'Algo salió mal'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
                
class GetEmptyExpedientesBySelectedArea(APIView):

    def get(self, request):

        area_id = self.request.query_params.get("area_id", None)
        expedientes = Expediente.objects.filter(idAreaProcedenciaN_id=area_id).exclude(Q(splitdocuments__isnull=False) | Q(idEstatus=4)).values('id','clave', 'folioSIO', 'idEstatus__nombre', 'idTipoMacroproceso__nombre', 'pori', 'reclamante', 'idInstitucion__nombre_corto', 'fechaCreacion', 'fechaApertura')

        return Response({
            'total': expedientes.count(),
            'expedientes': expedientes,
        })