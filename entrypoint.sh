# Realizar migraciones de la base de datos
python manage.py migrate --no-input

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

exec "$@"

# Iniciar Gunicorn con la configuración de 16 workers porque tenemos 16 núcleos en el server
                                        # EL SERVIDOR gunicorn ESPERA 14400 SEGUNDOS
gunicorn alfresco_clone.wsgi:application --bind 0.0.0.0:8000 --timeout 14400 --workers 16