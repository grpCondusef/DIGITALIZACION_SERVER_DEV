from django.db import models

# Create your models here.
    
class InstitucionesFinancieras(models.Model):
    clave_registro = models.CharField(max_length=20, null=True)
    denominacion_social = models.CharField(max_length=500)
    nombre_corto = models.CharField(max_length=200, null=True)
    rfc = models.CharField(max_length=20, null=True)
    estatus = models.CharField(max_length=500, null=True)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.denominacion_social
    
    
class EstatusCatalogo(models.Model):
    nombre = models.CharField(max_length=50)
    
    
class TipoMacroproceso(models.Model):
    clave = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50, null=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(null=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    idEstatus = models.ForeignKey(EstatusCatalogo,related_name='Status_Catalogo_TMacroproceso' , on_delete=models.CASCADE)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class TipoDocumental(models.Model):
    nombre = models.CharField(max_length=200)
    clave = models.CharField(max_length=10)
    vistaAsesor = models.IntegerField(null=True, blank=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(null=True, blank=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    idEstatus = models.ForeignKey(EstatusCatalogo,related_name='Status_Catalogo_TipoDocumental', on_delete=models.CASCADE)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class Macroproceso(models.Model):
    clave = models.CharField(max_length=10)
    nombre = models.CharField(max_length=256)
    idTipoMacroproceso = models.ForeignKey(TipoMacroproceso, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(null=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    idEstatus = models.ForeignKey(EstatusCatalogo,related_name='Status_Catalogo_Macroproceso' , on_delete=models.CASCADE)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class Proceso(models.Model):
    clave = models.CharField(max_length=10)
    nombre = models.CharField(max_length=256)
    idMacroproceso = models.ForeignKey(Macroproceso, on_delete=models.CASCADE)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(null=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    idEstatus = models.ForeignKey(EstatusCatalogo ,related_name='Status_Catalogo_Proceso' , on_delete=models.CASCADE)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class TipoOrdenamiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=50)
    
    
class Areas(models.Model):
    nombre = models.CharField(max_length=500)
    
    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['nombre'] #ORDENAR PONIENDO PRIMERO LOS ÚLTIMOS ARTÍCULOS PUBLICADOS
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class AreaSIO(models.Model):
    clave = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    nombreCorto = models.CharField(max_length=100, null=True)
    idArea = models.ForeignKey(Areas,related_name='area_AreaSIO', on_delete=models.CASCADE, null=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(null=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    idEstatus = models.ForeignKey(EstatusCatalogo,related_name='Status_Catalogo_AreaSIO', on_delete=models.CASCADE)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class Serie(models.Model):
    clave = models.CharField(max_length=10)
    nombre = models.CharField(max_length=256)
    idProceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    cierreExplicito = models.IntegerField(null=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(null=True)
    fechaActualizacion = models.DateTimeField(auto_now=True, null=True)
    idEstatus = models.ForeignKey(EstatusCatalogo,related_name='Status_Catalogo_Serie', on_delete=models.CASCADE)
    idOrdenamiento = models.ForeignKey(TipoOrdenamiento, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    

class VigenciaDocumental(models.Model):
    
    nombre = models.CharField(max_length=25, null=True)
    fechaInicio = models.DateTimeField(null=True, blank=True)
    fechaActualizacion = models.DateTimeField(null=True, blank=True)
    fechaFin = models.DateTimeField(null=True, blank=True)
    idEstatus = models.ForeignKey(EstatusCatalogo, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    

class SerieVigenciaDocumental(models.Model):
    
    idSerie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True)
    idVigenciaDocumental = models.ForeignKey(VigenciaDocumental, on_delete=models.CASCADE, null=True)
    anios = models.IntegerField(null=True, blank=True)
    meses = models.IntegerField(null=True, blank=True)
    dias = models.IntegerField(null=True, blank=True)
    fechaInicio = models.DateTimeField(null=True, blank=True)
    fechaActualizacion = models.DateTimeField(null=True, blank=True)
    fechaFin = models.DateTimeField(null=True, blank=True)
    idEstatus = models.ForeignKey(EstatusCatalogo, on_delete=models.CASCADE, null=True)
    
    #def __str__(self):
    #    # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
    #    return self.nombre
    

class ValoracionPrimaria(models.Model):
    
    nombre = models.CharField(max_length=25, null=True)
    fechaActualizacion = models.DateTimeField(null=True, blank=True)
    fechaFin = models.DateTimeField(null=True, blank=True)
    fechaInicio = models.DateTimeField(null=True, blank=True)
    idEstatus = models.ForeignKey(EstatusCatalogo, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    

class SerieValoracionPrimaria(models.Model):
    
    idSerie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True)
    idValoracionPrimaria = models.ForeignKey(ValoracionPrimaria, on_delete=models.CASCADE, null=True)
    fechaInicio = models.DateTimeField(null=True, blank=True)
    idEstatus = models.ForeignKey(EstatusCatalogo, on_delete=models.CASCADE, null=True)
    fechaActualizacion = models.DateTimeField(null=True, blank=True)
    fechaFin = models.DateTimeField(null=True, blank=True)
    
    #def __str__(self):
    #    # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
    #    return self.nombre

    
class AreaProcedenciaN(models.Model):
    claveAreaSIO = models.CharField(max_length=100, null=True)
    nombreAreaSIO = models.CharField(max_length=100, null=True)
    claveArea = models.CharField(max_length=100, null=True)
    nombreArea = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombreAreaSIO
    

class EstatusExpediente(models.Model):
    nombre = models.CharField(max_length=50)
       
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.nombre
    
    
class Expediente(models.Model):
    clave = models.CharField(max_length=100, null=True, blank=True, unique=True)
    idUsuarioCreador = models.ForeignKey('USER_APP.User', on_delete=models.CASCADE, null=True) #LO IMPORTAMOS ASI PORQUE NO NOS DEJA IMPORTAR "User" DE USER_APP.models
    idTipoMacroproceso = models.ForeignKey(TipoMacroproceso, on_delete=models.CASCADE, null=True)
    idMacroproceso = models.ForeignKey(Macroproceso, on_delete=models.CASCADE, null=True)
    idProceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, null=True)
    idSerie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True)
    idSubserie = models.CharField(max_length=100, null=True, blank=True)
    fechaCreacion = models.DateTimeField(blank=True, null=True)
    fechaApertura = models.DateTimeField(blank=True)
    fechaCierre = models.DateTimeField(null=True, blank=True)
    numeroLegajos = models.IntegerField(null=True, blank=True)
    numeroFojas = models.IntegerField(null=True, blank=True)
    resumenContenido = models.CharField(max_length=30000, null=True, blank=True)
    idAreaProcedenciaN = models.ForeignKey(Areas, on_delete=models.CASCADE, null=True)
    idAreaProcedenciaA = models.IntegerField(null=True, blank=True)
    folioSIO = models.CharField(max_length=500, null=True, blank=True)
    idAreaSIO = models.ForeignKey(AreaSIO, on_delete=models.CASCADE, null=True, blank=True)
    reclamante = models.CharField(max_length=300, null=True, blank=True)
    idInstitucion = models.ForeignKey(InstitucionesFinancieras, on_delete=models.CASCADE, null=True, blank=True)
    idEstatus = models.ForeignKey(EstatusExpediente, on_delete=models.CASCADE, null=True)
    instanciaProceso = models.CharField(max_length=10, null=True, blank=True)
    baseHistorico = models.CharField(max_length=50, null=True, blank=True)
    pori = models.CharField(max_length=20, null=True, blank=True)
    idUsuarioModificador = models.CharField(max_length=50, null=True, blank=True)
    fechaModificacion = models.DateTimeField(auto_now=True, null=True)
    institucionMig = models.CharField(max_length=68655, null=True, blank=True)
    processInstanceIDRC = models.CharField(max_length=50, null=True, blank=True)
    formatoSoporte = models.CharField(max_length=50, null=True, blank=True)
    sistema = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'
        ordering = ['-fechaCreacion'] #ORDENAR PONIENDO PRIMERO LOS ÚLTIMOS ARTÍCULOS PUBLICADOS
        
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.clave
    
    
class ExpedienteOptions(models.Model):
    idArea = models.ForeignKey(Areas, related_name='area_expediente_options', on_delete=models.CASCADE, null=True, blank=True)
    idTipoMacroproceso = models.ForeignKey(TipoMacroproceso, related_name='TipoMacroproceso_expediente_options', on_delete=models.CASCADE, null=True, blank=True)
    idMacroproceso = models.ForeignKey(Macroproceso, related_name='Macroproceso_options', on_delete=models.CASCADE, null=True, blank=True)
    idProceso = models.ForeignKey(Proceso, related_name='Proceso_options', on_delete=models.CASCADE, null=True, blank=True)
    idSerie = models.ForeignKey(Serie, related_name='Serie_options', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Add expediente option'
        verbose_name_plural = 'Add expediente options'
        ordering = ['-idArea'] #ORDENAR PONIENDO PRIMERO LOS ÚLTIMOS ARTÍCULOS PUBLICADOS
        
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.idArea.nombre
    
    
class AlfrescoCCA(models.Model):
    clave = models.CharField(max_length=100, null=True, blank=True)
    idTipoMacroproceso = models.ForeignKey(TipoMacroproceso, on_delete=models.CASCADE, null=True)
    idMacroproceso = models.ForeignKey(Macroproceso, on_delete=models.CASCADE, null=True)
    idProceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, null=True)
    idSerie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True)
    folioSIO = models.CharField(max_length=1500, null=True, blank=True)
    
    def __str__(self):
        # MOSTRAMOS LA DIRECCIÓN EN LA TABLA DE REGISTROS DE LA BASE DE DATOS DEL ADMINISTRADOR
        return self.clave