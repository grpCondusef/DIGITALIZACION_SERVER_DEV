#!/bin/bash
# Script para comprobar la sincronización de archivos entre host y container Docker en un proyecto Django

# Cambia estos valores según tu setup
CONTAINER_NAME="uridec_api"
CONTAINER_PATH="/app/archexpedientes"
HOST_PATH="./archexpedientes"
PRUEBA_NOMBRE="test_sync_$$.txt"

echo "==> Creando archivo de prueba en el host: $HOST_PATH/$PRUEBA_NOMBRE"
echo "Archivo de prueba creado desde el HOST el $(date)" > "$HOST_PATH/$PRUEBA_NOMBRE"

echo "==> Listando archivos en el container tras crear en el host..."
docker-compose exec $CONTAINER_NAME ls -l $CONTAINER_PATH | grep $PRUEBA_NOMBRE && echo "OK: ¡El archivo está en el container!" || echo "ERROR: El archivo NO está en el container."

echo "==> Creando archivo de prueba en el container: $CONTAINER_PATH/$PRUEBA_NOMBRE"
docker-compose exec $CONTAINER_NAME bash -c "echo 'Archivo de prueba creado desde el CONTAINER el $(date)' > $CONTAINER_PATH/$PRUEBA_NOMBRE"

echo "==> Listando archivos en el host tras crear en el container..."
ls -l $HOST_PATH | grep $PRUEBA_NOMBRE && echo "OK: ¡El archivo está en el host!" || echo "ERROR: El archivo NO está en el host."

echo "==> Limpiando archivos de prueba..."
rm -f "$HOST_PATH/$PRUEBA_NOMBRE"
docker-compose exec $CONTAINER_NAME rm -f "$CONTAINER_PATH/$PRUEBA_NOMBRE"

echo "==> Sincronización de archivos verificada."