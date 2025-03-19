import requests
from pathlib import Path

ENDPOINT = 'http://127.0.0.1:8000/digitalizacion/'
TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NDY5NDA4LCJpYXQiOjE2NzI5MzM0MDgsImp0aSI6ImIzMDk1MTVlNjQ2YzQwZjk4YjE4ZWQyM2ExOTE4OWQ4IiwidXNlcl9pZCI6M30.M-ZjFpIWJpVUN4PkEBsIYXq8b_ncbntjW4VHCSJMxuQ'
BASE_DIR = Path(__file__).resolve().parent


###################################### TESTING PARA AGREGAR DOCUMENTOS ######################################

def test_agregar_documentos_desde_sine():

    #Nos imprime la dirección en la que se encuentra
    print(BASE_DIR)

    headers = {
        'Authorization': TOKEN
    }

    # Path del archivo PDF que deseas enviar en la solicitud
    pdf_file_path = r'C:/Users/apescador/Desktop/DIGITALIZACION_SERVER/DIGITALIZACION_APP/api/tests/documentsTest/SINETEST.pdf'    

    # Construye el cuerpo de la solicitud con un archivo adjunto
    files = {
        'document': ('SINETEST.pdf', open(pdf_file_path, 'rb'), 'application/pdf')
    }

    #Datos que se utilizan para la prueba (son los datos que se incorporan desde el método POST)
    data = {
        'folioSIO': "VPT/DGESPF/DDEPO/2023/SIPRES-SIC-6/1554",
        'tipo_id': "1", 
        'user_id': "1"
    }

    response = requests.post(ENDPOINT + "send-document-sine/", data=data, files=files, headers=headers)

    # Verifica si la respuesta HTTP es código 200
    assert response.status_code == 200 
    data = response.json()
    assert data['folioSIO']
    assert data['tipo_id']
    assert data['mensaje'] == 'Documento procesado exitosamente.'
    


###################################### TESTING PARA ERRORES ######################################

def test_agregar_documentos_desde_sine_no_token():

    headers = {}

   # Path del archivo PDF que deseas enviar en la solicitud
    pdf_file_path = r'C:/Users/apescador/Desktop/DIGITALIZACION_SERVER/DIGITALIZACION_APP/api/tests/documentsTest/SINETEST.pdf'    

    # Construye el cuerpo de la solicitud con un archivo adjunto
    files = {
        'document': ('SINETEST.pdf', open(pdf_file_path, 'rb'), 'application/pdf')
    }

    #Datos que se utilizan para la prueba (son los datos que se incorporan desde el método POST)
    data = {
        'folioSIO': "VPT/DGESPF/DDEPO/2023/SIPRES-SIC-6/1554",
        'tipo_id': "1", 
        'user_id': "1"
    }

    response = requests.post(ENDPOINT + "send-document-sine/", files=files, headers=headers)

    # Verifica si la respuesta HTTP es código 400
    assert response.status_code == 401
    data = response.json()
    assert data['detail']
    assert data['detail'] == 'Las credenciales de autenticación no se proveyeron.'
    


def test_agregar_documentos_desde_sine_no_folioSio():

    headers = {
        'Authorization': TOKEN
    }

   # Path del archivo PDF que deseas enviar en la solicitud
    pdf_file_path = r'C:/Users/apescador/Desktop/DIGITALIZACION_SERVER/DIGITALIZACION_APP/api/tests/documentsTest/SINETEST.pdf'    

    # Construye el cuerpo de la solicitud con un archivo adjunto
    files = {
        'document': ('SINETEST.pdf', open(pdf_file_path, 'rb'), 'application/pdf')
    }

    #Datos que se utilizan para la prueba (son los datos que se incorporan desde el método POST)
    data = {
        'tipo_id': "1", 
        'user_id': "1"
    }

    response = requests.post(ENDPOINT + "send-document-sine/", data=data, files=files, headers=headers)

    # Verifica si la respuesta HTTP es código 400
    assert response.status_code == 400
    data = response.json()
    assert data['error']
    assert data['error'] == 'Faltan los siguientes campos obligatorios: folioSIO'



def test_agregar_documentos_desde_sine_no_tipoid():

    headers = {
        'Authorization': TOKEN
    }
    
    # Path del archivo PDF que deseas enviar en la solicitud
    pdf_file_path = r'C:/Users/apescador/Desktop/DIGITALIZACION_SERVER/DIGITALIZACION_APP/api/tests/documentsTest/SINETEST.pdf'    

    # Construye el cuerpo de la solicitud con un archivo adjunto
    files = {
        'document': ('SINETEST.pdf', open(pdf_file_path, 'rb'), 'application/pdf')
    }

    #Datos que se utilizan para la prueba (son los datos que se incorporan desde el método POST)
    data = {
        'folioSIO': "VPT/DGESPF/DDEPO/2023/SIPRES-SIC-6/1554",
        'user_id': "1"
    }

    response = requests.post(ENDPOINT + "send-document-sine/", data=data, files=files, headers=headers)

    # Verifica si la respuesta HTTP es código 400
    assert response.status_code == 400#
    data = response.json()#
    assert data['error']
    assert data['error'] == 'Faltan los siguientes campos obligatorios: tipo_id'



def test_agregar_documentos_desde_sine_no_userid():

    headers = {
        'Authorization': TOKEN
    }

    # Path del archivo PDF que deseas enviar en la solicitud
    pdf_file_path = r'C:/Users/apescador/Desktop/DIGITALIZACION_SERVER/DIGITALIZACION_APP/api/tests/documentsTest/SINETEST.pdf'    

    # Construye el cuerpo de la solicitud con un archivo adjunto
    files = {
        'document': ('SINETEST.pdf', open(pdf_file_path, 'rb'), 'application/pdf')
    }

    #Datos que se utilizan para la prueba (son los datos que se incorporan desde el método POST)
    data = {
        'folioSIO': "VPT/DGESPF/DDEPO/2023/SIPRES-SIC-6/1554",
        'tipo_id': "1"
    }

    response = requests.post(ENDPOINT + "send-document-sine/", data=data, files=files, headers=headers)

    # Verifica si la respuesta HTTP es código 500
    assert response.status_code == 400
    data = response.json()
    assert data['error']
    assert 'user_id' in data['error']
    


def test_agregar_documentos_desde_sine_no_files():

    headers = {
        'Authorization': TOKEN
    }

    # Construye el cuerpo de la solicitud con un archivo adjunto
    files = {}

    #Datos que se utilizan para la prueba (son los datos que se incorporan desde el método POST)
    data = {
        'folioSIO': "VPT/DGESPF/DDEPO/2023/SIPRES-SIC-6/1554",
        'tipo_id': "1", 
        'user_id': "1"
    }

    response = requests.post(ENDPOINT + "send-document-sine/", data=data, files=files, headers=headers)

    # Verifica si la respuesta HTTP es código 400
    assert response.status_code == 400
    data = response.json()
    assert data['error']
    assert data['error'] == 'Faltan los siguientes campos obligatorios: document'

    