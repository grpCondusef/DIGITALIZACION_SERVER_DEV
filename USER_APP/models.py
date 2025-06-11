from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from CATALOGOS.models import Areas, Expediente

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, password=None):

        if not username:
            raise ValueError('el usuario debe tener un username')

        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, password):
        user = self.create_user(
            username = username,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    area = models.ForeignKey(Areas ,related_name='user_area' , on_delete=models.CASCADE,null=True)
    areas_asociadas = models.ManyToManyField(Areas)
    CHOICES = (
        ('test', 'Test'),
        ('generica', 'Genérica'),
        ('personal', 'Personal'),
    )
    tipo_cuenta = models.CharField(max_length=256, choices=CHOICES, default='personal')
    crear_expedientes = models.BooleanField(null=True, default=False) 
    eliminar_expedientes = models.BooleanField(null=True, default=False) 
    subir_documentos = models.BooleanField(null=True, default=False) 
    consulta_completa = models.BooleanField(null=True, default=False)
    migrar_expediente = models.BooleanField(null=True, default=False)
    carga_masiva = models.BooleanField(null=True, default=False)
    eliminar_documentos = models.BooleanField(null=True, default=False)
    dashboard_uau = models.BooleanField(null=True, default=False)
    certificar_expediente = models.BooleanField(null=True, default=False)
    
    #campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None): #NOS MUESTRA SI ES ADMINISTRADOR
        return self.is_admin

    def has_module_perms(self, add_label):  #SI EL DE ARRIBA ES #True, SE EJECUTA ESTA DE AQUÍ
        return True


class Bitacora(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=600, null=True, blank=True)
    description = models.CharField(max_length=600, null=True, blank=True)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)