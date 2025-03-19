from rest_framework import serializers
from django.contrib.auth.models import User
from USER_APP.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True) #EL CLIENTE NO VA APODER VER MI PASSWORD, SOLAMENTE ESCRIBIRLO

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True} #TAMBIÉN SERÁ SOLAMENTE DE ESCRITURA
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2'] #PASSWORD DE CONFIRMACIÓN

        if password != password2:
            raise serializers.ValidationError({'error': 'El passwor de confirmacion no coincide'})

        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'El username del usuario ya existe'})

        account =User.objects.create_user(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )
        account.set_password = self.validated_data['password']

        #account.set_password(password)
        account.save()
        return account
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'