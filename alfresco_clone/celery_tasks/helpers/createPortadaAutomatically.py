from django.apps import apps
from DIGITALIZACION_APP.api.helpers.crearPortada import crear_portada
from pathlib import Path
import os



def getVigenciasIds(serieId):
    
    # Configurar Django después de la configuración de Celery
    from alfresco_clone.celery_config import app as celery_app
    celery_app.loader.import_default_modules()

    # Importar los modelos de Django después de la configuración de Celery
    SerieVigenciaDocumental = apps.get_model('CATALOGOS', 'SerieVigenciaDocumental')

# Consulta única para obtener las vigencias
    try:
        vigencias = SerieVigenciaDocumental.objects.filter(
            idSerie_id=serieId)
        # Asignación de las vigencias
        vigencia_ids = {1: None, 2: None, 3: None}
        for vigencia in vigencias:
            vigencia_ids[vigencia.idVigenciaDocumental_id] = {}

            vigencia_ids[vigencia.idVigenciaDocumental_id]["anios"] = vigencia.anios
            vigencia_ids[vigencia.idVigenciaDocumental_id]["meses"] = vigencia.meses
            vigencia_ids[vigencia.idVigenciaDocumental_id]["dias"] = vigencia.dias
            
        return vigencia_ids
    except Exception as e:
        print(e)
        return e
            
    
def getValoresDocumentales(serieId):
    # Configurar Django después de la configuración de Celery
    from alfresco_clone.celery_config import app as celery_app
    celery_app.loader.import_default_modules()
    
    SerieValoracionPrimaria = apps.get_model('CATALOGOS', 'SerieValoracionPrimaria')
    try:
        valoresDocumentales_array = [valor.idValoracionPrimaria.nombre for valor in SerieValoracionPrimaria.objects.filter(idSerie_id=serieId)]
        return valoresDocumentales_array
    except Exception as e:
        print(e)
        return e

from datetime import datetime, timedelta

def createPortadaPath(clave):
    
    actual_year = datetime.now().year
    actual_month = datetime.now().month
    actual_day = datetime.now().day
    
    path = 'uridec/pdf_portadas/{}/{}/{}/{}_portada.pdf'.format(actual_year, actual_month, actual_day, clave)
    return path
    
    
def searchPortada(expedienteId):
    
    # Configurar Django después de la configuración de Celery
    from alfresco_clone.celery_config import app as celery_app
    celery_app.loader.import_default_modules()
    
    Portadas = apps.get_model('DIGITALIZACION_APP', 'Portadas')
    
    portada = Portadas.objects.filter(expediente__id=expedienteId)
    
    # Comprobar si hay resultados
    if portada.exists():
        return True
    else:
        return False

        
def initCreatePortada():
    
    # Configurar Django después de la configuración de Celery
    from alfresco_clone.celery_config import app as celery_app
    celery_app.loader.import_default_modules()

    # Importar los modelos de Django después de la configuración de Celery
    Expediente = apps.get_model('CATALOGOS', 'Expediente')
    
    
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    expedientes = Expediente.objects.all()
    
    for expediente in expedientes:
        clave = expediente.clave
        serie_id = expediente.idSerie.id
        expediente_id = expediente.id
        
        vigencias_ids = getVigenciasIds(serie_id)
        valores_documentales = getValoresDocumentales(serie_id)
        portada_path = createPortadaPath(clave)
        portada_exists = searchPortada(expediente_id)
        
        # ESTABLECER EL PATH EN DONDE ESTÁN LAS IMÁGENES DE LA PORTADA
        path_img = os.path.join(BASE_DIR, 'archexpedientes/img/')
        
        #print(vigencias_ids)
        
        crear_portada(BASE_DIR, path_img, clave, expediente, vigencias_ids, valores_documentales, serie_id)
        