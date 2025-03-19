# python3 -m pytest -s
import requests

ENDPOINT = 'http://127.0.0.1:8000/catalogos/'

TOKEN_VALIDO = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NDY5NDA4LCJpYXQiOjE2NzI5MzM0MDgsImp0aSI6ImIzMDk1MTVlNjQ2YzQwZjk4YjE4ZWQyM2ExOTE4OWQ4IiwidXNlcl9pZCI6M30.M-ZjFpIWJpVUN4PkEBsIYXq8b_ncbntjW4VHCSJMxuQ'

TOKEN_NO_VALIDO = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgk'

    
    
def test_tipo_macroproceso_options_list():
    
    area_id = 3500500
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'tipomacroproceso-options-view/?area_id={area_id}', headers=headers)

    assert response.status_code == 200
    
    data = response.json()

    assert data['area']
    assert data['tipo_macroproceso']
    assert data['tipo_macroproceso'][0]['tipo_macroproceso_id']
    assert data['tipo_macroproceso'][0]['tipo_macroproceso_nombre']
    
    
def test_tipo_macroproceso_options_list_no_area():
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'tipomacroproceso-options-view/', headers=headers)

    assert response.status_code == 400
    
    data = response.json()

    assert data['error']
    assert data['error'] == 'El id del área no fue proporcionado'
    
    
def test_tipo_macroproceso_options_list_no_token():
    
    response = requests.get(ENDPOINT + f'tipomacroproceso-options-view/')

    assert response.status_code == 401

    data = response.json()

    assert data['detail']
    assert data['detail'] == 'Las credenciales de autenticación no se proveyeron.'


    
def test_no_exist_tipo_macroproceso_options():
    
    area_id = 2
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'tipomacroproceso-options-view/?area_id={area_id}', headers=headers)
    
    assert response.status_code == 400

    data = response.json()

    assert data['error'] 
    assert data['error'] == 'No existen registros para esta consulta'
    


def test_macroproceso_options_list():
    
    area_id = 3410110
    tipomacroproceso_id = 1
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'macroproceso-options-view/?tipomacroproceso_id={tipomacroproceso_id}&area_id={area_id}', headers=headers)
    
    data = response.json()
    
    assert data['macroprocesos']
    assert data['macroprocesos'][0]['macroproceso_id']
    assert data['macroprocesos'][0]['macroproceso_nombre']
    


def test_macroproceso_options_list_no_token():
    
    area_id = 3410110
    tipomacroproceso_id = 1
    
    response = requests.get(ENDPOINT + f'macroproceso-options-view/?tipomacroproceso_id={tipomacroproceso_id}&area_id={area_id}')

    assert response.status_code == 401

    data = response.json()

    assert data['detail']
    assert data['detail'] == 'Las credenciales de autenticación no se proveyeron.'


    
def test_macroproceso_options_no_tipomacroproceso_id():
    
    area_id = 1
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'macroproceso-options-view/?area_id={area_id}', headers=headers)
    
    assert response.status_code == 400
    
    data = response.json()
    
    assert data['error']
    assert data['error'] == 'Es necesario proporcionar: tipomacroproceso_id'
    
    
    
def test_macroproceso_options_no_area_id():
    
    tipomacroproceso_id = 3410110
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'macroproceso-options-view/?tipomacroproceso_id={tipomacroproceso_id}', headers=headers)
    
    assert response.status_code == 400
    
    data = response.json()
    
    assert data['error']
    assert data['error'] == 'Es necesario proporcionar: area_id'    
        


def test_macroproceso_options_list():
    
    area_id = 1
    tipomacroproceso_id = 1
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'macroproceso-options-view/?tipomacroproceso_id={tipomacroproceso_id}&area_id={area_id}', headers=headers)
    
    data = response.json()
    
    assert data['error']
    assert data['error'] == 'No existen registros para esta consulta'

    
    
def test_proceso_options_list():
    
    area_id = 3410110
    tipomacroproceso_id = 1
    idMacroproceso_id = 2
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'proceso-options-view/?tipomacroproceso_id={tipomacroproceso_id}&macroproceso_id={idMacroproceso_id}&area_id={area_id}', headers=headers)

    assert response.status_code == 200
    
    data = response.json()
    
    assert data['procesos']
    assert data['procesos'][0]['proceso_id']
    assert data['procesos'][0]['proceso_nombre']
    
    
def test_serie_options_list():
    
    area_id = 3410110
    tipomacroproceso_id = 1
    idMacroproceso_id = 2
    idProceso_id = 4
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + f'serie-options-view/?tipomacroproceso_id={tipomacroproceso_id}&macroproceso_id={idMacroproceso_id}&proceso_id={idProceso_id}&area_id={area_id}', headers=headers)

    assert response.status_code == 200
    
    data = response.json()
    
    assert data['series']
    assert data['series'][0]['serie_id']
    assert data['series'][0]['serie_nombre']
    
    
def test_if_list():
    
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgko'
    }
    
    response = requests.get(ENDPOINT + 'if-lista-view/', headers=headers)

    assert response.status_code == 200
    
    data = response.json()
    
    assert data['instituciones_financieras']
    assert data['instituciones_financieras'][0]['institucionFinaciera_id']
    assert data['instituciones_financieras'][0]['denominacion_social']
    assert data['instituciones_financieras'][0]['estatus']