import uuid
import os
from datetime import datetime

from django.db import models
from CATALOGOS.models import Expediente, TipoDocumental, TipoMacroproceso
from USER_APP.models import User

def image_upload_path(instance, filename):
    now = datetime.now()
    cadena_fecha = now.strftime("%Y-%m-%d-%H-%M-%S")
    cadena_unique_identifier = str(uuid.uuid4())
    new_filename = '{}_{}.pdf'.format(cadena_fecha, cadena_unique_identifier)
    actual_year = datetime.now().year
    actual_month = datetime.now().month
    actual_day = datetime.now().day
    
    directory = os.path.join('uridec', 'original_documents', str(actual_year), str(actual_month), str(actual_day))
    return os.path.join(directory, new_filename)


# Create your models here.
class OriginalDocuments(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey( User, editable=False, on_delete=models.CASCADE, null=True)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    uploadedFile = models.FileField(upload_to = image_upload_path, blank=True, null=True,)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-date_creation'] #ORDENAR PONIENDO PRIMERO LOS ÚLTIMOS PUBLICADOS
    
    def __str__(self):
        return self.title

class Portadas(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey( User, editable=False, on_delete=models.CASCADE, null=True)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    path = models.CharField(max_length=200, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Portada'
        verbose_name_plural = 'Portadas'
        ordering = ['-date_creation'] #ORDENAR PONIENDO PRIMERO LOS ÚLTIMOS PUBLICADOS
    
    def __str__(self):
        return self.name

class SplitDocuments(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey( User, editable=False, on_delete=models.CASCADE, null=True)
    tipo = models.ForeignKey(TipoDocumental, on_delete=models.CASCADE, null=True,)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    path = models.CharField(max_length=200, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    docIndex = models.IntegerField(null=True, default=0)
    
    
    class Meta:
        verbose_name = 'Split Document'
        verbose_name_plural = 'Split Documents'
        ordering = ['-date_creation'] #ORDENAR PONIENDO PRIMERO LOS ÚLTIMOS PUBLICADOS
    
    def __str__(self):
        return self.name
