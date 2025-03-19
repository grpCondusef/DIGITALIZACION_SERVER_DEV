# python3 -m pytest -s
import requests

ENDPOINT = 'http://127.0.0.1:8000/users/'

TOKEN_VALIDO = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NDY5NDA4LCJpYXQiOjE2NzI5MzM0MDgsImp0aSI6ImIzMDk1MTVlNjQ2YzQwZjk4YjE4ZWQyM2ExOTE4OWQ4IiwidXNlcl9pZCI6M30.M-ZjFpIWJpVUN4PkEBsIYXq8b_ncbntjW4VHCSJMxuQ'

TOKEN_NO_VALIDO = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNTA1Njk1LCJpYXQiOjE2Njg5Njk2OTUsImp0aSI6IjI1NGZhODdjOTNkYTRlNTNiYzQ4MzBkYjNlNDZhYjlhIiwidXNlcl9pZCI6MX0.Ifj23wEIRiV52B7jzugitrSAnv4U6kf55HKnQLwcgk'


def test_create_user():

    payload = {
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "password": "test",
            "password2": "test"
        }
    
    response = requests.post(ENDPOINT + 'create-user/', json=payload)

    assert response.status_code == 201
    assert response.json()["msg"] == "El usuario ha sido creado correctamente"
    assert response.json()["token"]['refresh']
    assert response.json()["token"]['access']
    


def test_create_user_verify_new_user_data():
    payload = {
        "username": "tests",
        "first_name": "test",
        "last_name": "test",
        "password": "test",
        "password2": "test2"
    }

    # Verificar que con cualquier campo que falte devuelva el mismo código de error HTTP y el mismo mensaje
    for field in payload:
        # Excluir password2 del bucle
        if field == 'password2':
            continue

        # Elimina un campo de la carga útil
        payload_without_field = {key: value for key, value in payload.items() if key != field}

        response = requests.post(ENDPOINT + 'create-user/', json=payload_without_field)
        
        assert response.status_code == 400
        assert response.json()["error"] == "Todos los campos son obligatorios"
    
    # Verificar que el password y el password del usuario son iguales
    response = requests.post(ENDPOINT + 'create-user/', json=payload)
    assert response.status_code == 400
    assert response.json()["error"] == "Las contraseñas deben coincidir"
        
         
    
def test_login():

    payload = {
            "username": "sa",
            "password": "0neOne$1"
        }
    
    response = requests.post(ENDPOINT + 'login/',
                            json=payload)

    assert response.status_code == 200


def test_login_not_username_or_password():

    payload_without_username = {
        "password": "0neOne$1"
    }
    response = requests.post(ENDPOINT + 'login/', json=payload_without_username)
    assert response.status_code == 400
    assert response.json()["error"] == "El usuario y la contraseña son obligatorios"

    payload_without_password = {
        "username": "sa"
    }
    response = requests.post(ENDPOINT + 'login/', json=payload_without_password)
    assert response.status_code == 400
    assert response.json()["error"] == "El usuario y la contraseña son obligatorios"


def test_get_user_info():

    headers = {
        'Authorization': TOKEN_VALIDO
    }

    response = requests.get(ENDPOINT + 'user-info/',
                            headers=headers)

    assert response.status_code == 200


def test_get_user_info_validate_token():

    headers = {
        'Authorization': TOKEN_NO_VALIDO
    }

    response = requests.get(ENDPOINT + 'user-info/')

    assert response.status_code == 400
    assert response.json()["error"] == "Es necesario proporcionar el token de acceso."
    
    response = requests.get(ENDPOINT + 'user-info/', headers=headers)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "El token dado no es valido para ningun tipo de token"
    
    
def test_change_password():
    
    payload = {
            "username": "test",
            'password': 'test',
            'password2': 'test'
        }
    
    response = requests.put(ENDPOINT + 'change-password/', json=payload)
    
    assert response.status_code == 200
    
    
def test_change_password_validate_data():
    
    wrong_username_payload = {
            "username": "wrong",
            'password': 'test',
            'password2': 'test'
        }
    
    response = requests.put(ENDPOINT + 'change-password/', json=wrong_username_payload)
    
    assert response.status_code == 400
    assert response.json()['error'] == 'El usuario no existe'
    
    different_passwords_payload = {
        "username": "test",
        'password': 'test',
        'password2': 'wrong_password'
    }
    
    response = requests.put(ENDPOINT + 'change-password/', json=different_passwords_payload)
    
    assert response.status_code == 400
    assert response.json()['error'] == 'Las contraseñas deben coincidir'
    
    incomplete_fields_payload = {
        "username": "test",
        'password': 'test',
        'password2': 'test'
    }
    
    for field in incomplete_fields_payload:

        # Elimina un campo de la carga útil
        payload_without_field = {key: value for key, value in incomplete_fields_payload.items() if key != field}

        response = requests.put(ENDPOINT + 'change-password/', json=payload_without_field)
        
        assert response.status_code == 400
        assert response.json()["error"] == "Todos los campos son obligatorios"
    


def test_logout():

    payload = {
            "username": "sa"
        }
    
    response = requests.post(ENDPOINT + 'logout/',
                            json=payload)

    assert response.status_code == 200