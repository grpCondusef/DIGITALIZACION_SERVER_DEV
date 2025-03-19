from datetime import timedelta
from celery.schedules import crontab
from alfresco_clone.celery_config import app
from .helpers.createPortadaAutomatically import initCreatePortada


app.conf.beat_schedule = {
    'task1':{
        'task': 'alfresco_clone.celery_tasks.ex11_task_scheduling.task1',
        #'schedule': timedelta(seconds=600)
        'schedule': crontab(minute=10, hour=16),  # Ejecutar a la 1:25 PM todos los días
    },
    'task2':{
        'task': 'alfresco_clone.celery_tasks.ex11_task_scheduling.task2',
        'schedule': timedelta(seconds=5)
    }
}

@app.task(queue='tasks')
def task1():
    #initCreatePortada()
    print ('Creando portada')


@app.task(queue='tasks')
def task2():
    print ('Running task2')
    