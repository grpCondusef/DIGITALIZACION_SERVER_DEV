# import json
# from kafka import KafkaProducer
#
#
# ORDER_KAFKA_TOPIC = 'confirm_uploading'
# producer = KafkaProducer(bootstrap_servers='10.33.200.115:29092')
#
#
# def sendConfirmationEmail(respuesta, username, file, clave_expediente, expediente_id):
#
#    # ================  CONFIGURACIÓN KAFKA ==================
#    kafka_data = {
#        'destinationMail': '{}@condusef.gob.mx'.format(username),
#        'msg': 'El documento {} fue agregado exitosamente al expediente {} por el usuario {}'.format(file, clave_expediente, username),
#        'clave': clave_expediente,
#        'username': username,
#        'expedienteLink': 'http://{}/expediente/documents/{}'.format('10.33.200.115', expediente_id),
#        'uploaded_files': respuesta['uploaded_files']
#    }
#
#    # Enviar el pedido al tópico (canal de datos) Kafka 'order_details' después de codificarlo como JSON
#    producer.send(ORDER_KAFKA_TOPIC, json.dumps(kafka_data).encode('utf-8'))


import json
import os
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

ORDER_KAFKA_TOPIC = 'confirm_uploading'


def get_kafka_producer():
    """
    Crea y retorna un productor de Kafka si está habilitado.
    Evita romper la app si Kafka no está disponible.
    """
    if os.environ.get('DISABLE_KAFKA') == 'true':
        print("[INFO] Kafka deshabilitado por variable de entorno.")
        return None
    try:
        return KafkaProducer(bootstrap_servers='10.33.200.115:29092')
    except NoBrokersAvailable as e:
        print(f"[WARN] No se pudo conectar a Kafka: {e}")
        return None


def sendConfirmationEmail(respuesta, username, file, clave_expediente, expediente_id):
    producer = get_kafka_producer()
    if not producer:
        print("[INFO] No se envió mensaje a Kafka.")
        return

    kafka_data = {
        'destinationMail': f'{username}@condusef.gob.mx',
        'msg': f'El documento {file} fue agregado exitosamente al expediente {clave_expediente} por el usuario {username}',
        'clave': clave_expediente,
        'username': username,
        'expedienteLink': f'http://10.33.200.115/expediente/documents/{expediente_id}',
        'uploaded_files': respuesta['uploaded_files']
    }

    producer.send(ORDER_KAFKA_TOPIC, json.dumps(kafka_data).encode('utf-8'))
    producer.flush()
    producer.close()
