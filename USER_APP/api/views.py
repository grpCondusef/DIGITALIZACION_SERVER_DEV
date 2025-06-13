from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from USER_APP.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
#from user_app import models
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken #CON ESTA LIBRERÍA VAMOS A GENERAR EL TOKEN
from django.contrib import auth
from django.forms.models import model_to_dict
from USER_APP.models import User, Bitacora
from CATALOGOS.models import AreaSIO



class CreateUserView(APIView):
    
    def post(self, request):
            
            data = {}
            
            # VERIFICAR QUE VIENEN TODOS LOS CAMPOS OBLIGATORIOS
            if 'username' not in request.data or 'first_name' not in request.data or not 'last_name' in request.data or not 'password' in request.data or not 'password2' in request.data:
                data['error'] = "Todos los campos son obligatorios"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            username = str(request.data['username'])
            first_name = str(request.data['first_name'])
            last_name = str(request.data['last_name'])
            password = str(request.data['password'])
            
            confirm_password = str(request.data['password2'])
            
            # VERIFICAR QUE NO EXISTE OTRO USUARIO CON EL MISMO "username"
            if User.objects.filter(username=username).exists():
                
                data['error'] = 'Ya existe un usuario con el mismo username'
                return Response(data, status.HTTP_400_BAD_REQUEST)
            
            # CONFIRMAR QUE AMBAS CONTRASEÑAS SON IGUALES
            if password == confirm_password:
                
                # Generar el hash de la contraseña utilizando pbkdf2_sha256
                hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256')
                
                try:
                    new_user = User.objects.create(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=hashed_password
                    )
                     
                    data['msg'] = 'El usuario ha sido creado correctamente'
                    
                    refresh = RefreshToken.for_user(new_user) #CREAMOS EL TOKEN
                    data['token'] = { #AGREGAMOS LA INFORMACIÓN DEL TOKEN A LA VARIABLE "data"
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                         
                    return Response(data, status.HTTP_201_CREATED)
                     
                except Exception as e:
                    print(e)
                    data['error'] = 'Parece que ha habido un error al intentar crear un nuevo usuario'
                    return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            else:
                data['error']= 'Las contraseñas deben coincidir'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    
    def post(self, request):
        data = {}
        if request.method=='POST':
            password = request.data.get('password')
            username = request.data.get('username')
            account = auth.authenticate(username=username, password=password)
            if not username or not password:
                data['error'] = "El usuario y la contraseña son obligatorios"
                
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            areas_asociadas_array = []
            if account is not None:
                data['response']='El Login fue exitoso'
                data['username']=account.username
                data['first_name']=account.first_name
                data['last_name']=account.last_name
                data['area']=account.area.nombre
                data['area_id']=account.area.id
                area_sio = AreaSIO.objects.filter(idArea_id=account.area.id, nombre__contains=account.area.nombre)
                for area in area_sio:
                    data['idAreaSIO'] = area.id
                data['tipo_cuenta']=account.tipo_cuenta
                data['crear_expedientes']=account.crear_expedientes
                data['eliminar_expedientes']=account.eliminar_expedientes
                data['subir_documentos']=account.subir_documentos
                data['consulta_completa']=account.consulta_completa
                data['migrar_expediente']=account.migrar_expediente
                data['carga_masiva']=account.carga_masiva
                data['eliminar_documentos']=account.eliminar_documentos
                data['dashboard_uau']=account.dashboard_uau
                data['certificar_expediente']=account.certificar_expediente
                areas_asociadas = account.areas_asociadas.all() #ESTA ES UNA TABLA INTERMEDIA
                for area in areas_asociadas:
                    areas_asociadas_array.append(model_to_dict(area))
            
                data['areas_asociadas']=areas_asociadas_array
                refresh = RefreshToken.for_user(account)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return Response(data)
            else:
                data['error'] = "Credenciales incorrectas"
                return Response(data, status.HTTP_400_BAD_REQUEST)
            
            
class ChangePasswordView(APIView):
    
    def put(self, request):
            
            data = {}
            
            # VERIFICAR QUE VIENEN TODOS LOS CAMPOS OBLIGATORIOS
            if 'username' not in request.data or not 'password' in request.data or not 'password2' in request.data:
                data['error'] = "Todos los campos son obligatorios"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            username = str(request.data['username'])
            password = str(request.data['password'])
            
            confirm_password = str(request.data['password2'])
            
            # VERIFICAR QUE EL USUARIO EXISTE
            if User.objects.filter(username=username).exists():
                
                # VERIFICAR QUE LAS PASSWORDS COINCIDEN
                if password == confirm_password:
                    
                    # Generar el hash de la contraseña utilizando pbkdf2_sha256
                    hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256')
                    
                    try:
                        User.objects.filter(username=username).update(password=hashed_password)
                        
                        data['msg'] = 'La contraseña ha sido modificada correctamente'
                        
                        return Response(data, status.HTTP_200_OK)
                        
                    except Exception as e:
                        print(e)
                        data['error'] = 'Parece que ha habido un error al intentar modificar la contraseña'
                        return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    data['error']= 'Las contraseñas deben coincidir'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                data['error']= 'El usuario no existe'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            
class UpdatePasswordByUserView(APIView):
    
    def put(self, request):
            
            data = {}
            
            # VERIFICAR QUE VIENEN TODOS LOS CAMPOS OBLIGATORIOS
            if 'username' not in request.data or not 'password' in request.data or not 'new_password' in request.data or not 'confirm_password' in request.data:
                data['error'] = "Todos los campos son obligatorios"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            username = str(request.data['username'])
            password = str(request.data['password'])            
            new_password = str(request.data['new_password'])            
            confirm_password = str(request.data['confirm_password'])
            
            account = auth.authenticate(username=username, password=password)
            
            if account is not None:
                # VERIFICAR QUE EL USUARIO EXISTE
                if User.objects.filter(username=username).exists():
                    
                    # VERIFICAR QUE LAS PASSWORDS COINCIDEN
                    if new_password == confirm_password:
                        
                        # Generar el hash de la contraseña utilizando pbkdf2_sha256
                        hashed_password = make_password(new_password, salt=None, hasher='pbkdf2_sha256')
                        
                        try:
                            User.objects.filter(username=username).update(password=hashed_password)
                            
                            data['msg'] = 'La contraseña ha sido modificada correctamente'
                            
                            return Response(data, status.HTTP_200_OK)
                            
                        except Exception as e:
                            print(e)
                            data['error'] = 'Parece que ha habido un error al intentar modificar la contraseña'
                            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        data['error']= 'Las contraseñas deben coincidir'
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                else:
                    data['error']= 'El usuario no existe'
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['error'] = "Credenciales incorrectas"
                return Response(data, status.HTTP_400_BAD_REQUEST)
 
from USER_APP.api.helpers.decryptResetPasswordToken import decrypt_token
class ResetForgotPasswordView(APIView):
    def post(self, request):
        
        data = {}
        token = str(request.data['token'])
        password = str(request.data['password'])
        username = decrypt_token(token, 3)
        
        try:
            # Generar el hash de la contraseña utilizando pbkdf2_sha256
            hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256')
            
            User.objects.filter(username=username).update(password=hashed_password)
            
            data['msg'] = 'La contraseña ha sido reestablecida correctamente'
            return Response(data)
        except User.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        

class UserInfoView(APIView):
    
    # ----------OBTENER TODOS LOS REGISTROS DE LA BASE DE DATOS------------------------
    def get(self, request):
        
        user_id = self.request.user.id
        data = {}
        
        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if not request.auth:
            data['error'] = "Es necesario proporcionar el token de acceso."
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            users = User.objects.filter(id=user_id)        
        except Exception as e:
            data['error'] = 'Parece que ha habido un error al consultar los datos del usuarios'
            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        areas_asociadas_array = []
        for user in users:
            data['id']=user.id
            data['username']=user.username
            data['first_name']=user.first_name
            data['last_name']=user.last_name
            data['area']=user.area.nombre
            data['area_id']=user.area.id
            area_sio = AreaSIO.objects.filter(idArea_id=user.area.id, nombre__contains=user.area.nombre)
            for j in area_sio:
                data['idAreaSIO'] = j.id
            data['tipo_cuenta']=user.tipo_cuenta
            data['crear_expedientes']=user.crear_expedientes
            data['eliminar_expedientes']=user.eliminar_expedientes
            data['subir_documentos']=user.subir_documentos
            data['consulta_completa']=user.consulta_completa
            data['migrar_expediente']=user.migrar_expediente
            data['carga_masiva']=user.carga_masiva
            data['eliminar_documentos']=user.eliminar_documentos
            data['dashboard_uau']=user.dashboard_uau
            data['certificar_expediente']=user.certificar_expediente
            areas_asociadas = user.areas_asociadas.all() #ESTA ES UNA TABLA INTERMEDIA
            for area in areas_asociadas:
                areas_asociadas_array.append(model_to_dict(area))
        
        data['areas_asociadas']=areas_asociadas_array
                
        return Response(data, status=status.HTTP_200_OK)
        
        


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data.get('username', ''))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'msg': 'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe el usuario'}, status=status.HTTP_400_BAD_REQUEST)


    
    
class AddBitacoraRegistro(APIView):
    
    def post(self, request):
        
        user_id = self.request.user.id
        data = self.request.data
        
        try:
            Bitacora.objects.create(
                user_id=user_id,
                action=data['action'],
                description=data['description'],
                expediente_id=data['expediente'] 
                )
            return Response({'msg': 'Registro en bitácora agregado exitosamente!!'},status=status.HTTP_201_CREATED)
        except:
            return Response(
            {'error': 'Parece que ha ocurrido un error!!!'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        