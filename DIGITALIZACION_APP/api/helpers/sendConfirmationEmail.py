import json
from kafka import KafkaProducer


ORDER_KAFKA_TOPIC = 'confirm_uploading'
producer = KafkaProducer(bootstrap_servers='10.33.200.115:29092')


def sendConfirmationEmail(respuesta, username, file, clave_expediente, expediente_id):

    # ================  CONFIGURACIÓN KAFKA ==================
    kafka_data = {
            'destinationMail': '{}@condusef.gob.mx'.format(username),
            'msg': 'El documento {} fue agregado exitosamente al expediente {} por el usuario {}'.format(file, clave_expediente, username),
            'clave': clave_expediente,
            'username': username,
            'expedienteLink': 'http://{}/expediente/documents/{}'.format('10.33.200.115', expediente_id),
            'uploaded_files': respuesta['uploaded_files']
        }  

    # Enviar el pedido al tópico (canal de datos) Kafka 'order_details' después de codificarlo como JSON
    producer.send(ORDER_KAFKA_TOPIC, json.dumps(kafka_data).encode('utf-8'))