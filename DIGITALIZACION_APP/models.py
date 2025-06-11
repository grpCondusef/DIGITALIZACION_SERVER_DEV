import uuid
import os
from datetime import datetime

from django.db import models
from CATALOGOS.models import Expediente, TipoDocumental, Areas
from USER_APP.models import User

def certificacion_upload_path(instance, filename):
    # Guarda los archivos en una carpeta por año/mes/expediente
    from datetime import datetime
    now = datetime.now()
    directory = f'uridec/certificaciones/{now.year}/{now.month}/{instance.expediente.id}/'
    return f"{directory}{filename}"

class CertificacionExpediente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificaciones')
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, null=True)
    fecha_certificacion = models.DateTimeField(auto_now_add=True)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    folio_expediente = models.CharField(max_length=500)  # Puedes obtenerlo de expediente.folioSIO
    recurrente = models.CharField(max_length=500)
    pdf_certificado = models.FileField(upload_to=certificacion_upload_path, null=True, blank=True)
    pdf_recurso_revision = models.FileField(upload_to=certificacion_upload_path, null=True, blank=True)
    fecha_recepcion_recurso = models.DateField(null=True, blank=True)
    fecha_envio_dgsl = models.DateField(null=True, blank=True)
    firmado = models.BooleanField(default=False)
    pdf_certificado_firmado = models.FileField(upload_to=certificacion_upload_path, null=True, blank=True)
    notificacion_enviada = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Certificación de Expediente'
        verbose_name_plural = 'Certificaciones de Expedientes'
        ordering = ['-fecha_certificacion']
    
    def __str__(self):
        return f"Certificación de {self.expediente} por {self.usuario} ({self.fecha_certificacion.strftime('%Y-%m-%d')})"
    
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
