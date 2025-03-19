# Use the official Python base image
FROM python:3.9
# Instalar libgl1-mesa-glx y libpq-dev
RUN apt-get update && apt-get install -y libgl1-mesa-glx libpq-dev
# Establecer el directorio de trabajo en el contenedor
WORKDIR /app
# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .
# Instalar las dependencias
RUN pip install -r requirements.txt
# Copiar todo al directorio de trabajo
COPY . /app
# Copiar el script de entrada al directorio raíz
COPY ./entrypoint.sh /entrypoint.sh
# Establecer el script de entrada como punto de entrada del contenedor
ENTRYPOINT ["sh", "/entrypoint.sh"]
