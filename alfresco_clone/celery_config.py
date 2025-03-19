import os
import time
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from celery import Celery
from kombu import Queue, Exchange

# Establecer la variable de entorno para utilizar la configuración de Djang
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfresco_clone.settings') #LO COPIAMOS DEL 
                                                                #ARCHIVO settings.py
        
# Crea una instancia de la aplicación Celery                                                                
app = Celery("alfresco_clone")# VA EL NOMBRE DE LA CARPETA EN DONDE 
                        #ESTA EL ARCHIVO settings.py      
                        
# Configuración de Celery                         
app.config_from_object("django.conf:settings", namespace="CELERY")

# Configuración de Sentry
sentry_dsn = 'https://d8a9332f33f9ee00bdf59d5dbb56243c@o4505825921204224.ingest.sentry.io/4505828344725504'
sentry_sdk.init(dsn=sentry_dsn, integrations=[CeleryIntegration()])


# Definición de la cola de tareas con una prioridad máxima de 10
app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
    Queue('dead_letter', routing_key='dead_letter')
]

# Permite que las tareas confirmen su finalización después de que los resultados se devuelvan al cliente
app.conf.task_acks_late = True
# Establece la prioridad predeterminada para las tareas en 5
app.conf.task_default_priority = 5
# Multiplicador para ajustar la cantidad de tareas que se pre-cargan en paralelo por proceso de trabajador
app.conf.worker_prefetch_multiplier = 1
# Establece el número de tareas que un trabajador puede manejar simultáneamente
app.conf.worker_concurrency = 1


# Obtiene la ruta base del directorio actual
base_dir = os.getcwd()
# Crea una ruta al directorio que contiene los archivos de tareas de Celery
task_folder = os.path.join(base_dir, 'alfresco_clone', 'celery_tasks')


# Comprueba si la carpeta de tareas existe y es un directorio
if os.path.exists(task_folder) and os.path.isdir(task_folder):

    # Lista para almacenar los nombres de los módulos de tareas
    task_modules = []

    # Itera a través de los archivos en la carpeta de tareas
    for filename in os.listdir(task_folder):
        # Verifica si el nombre de archivo comienza con 'ex' y termina con '.py'
        if filename.startswith('ex') and filename.endswith('.py'):
            # Construye el nombre del módulo basado en el nombre del archivo
            module_name = f'alfresco_clone.celery_tasks.{filename[:-3]}'
            
            # Importa el módulo de tareas dinámicamente
            module = __import__(module_name, fromlist=['*'])

            # Itera a través de los objetos en el módulo
            for name in dir(module):
                # Obtiene el objeto por nombre
                obj = getattr(module, name)
                # Verifica si el objeto es una función y comienza con 'my_task'
                if callable(obj) and name.startswith('my_task'):
                    # Agrega el nombre de la tarea al listado de módulos
                    task_modules.append(f'{module_name}.{name}')



# Configura la aplicación para autodescubrir las tareas en los módulos identificados
app.autodiscover_tasks(task_modules)