"""
Django settings for alfresco_clone project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=$1gm6oj+6usy)ug-96k$j2(g0x4%q=$+h3w*lo#_l83#(keaj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# ========== PARA ELIMINAR ERROR DE CSRF QUE APARECIÓ CON LA DOCKERIZACIÓN DE LA API ===========
CSRF_TRUSTED_ORIGINS = ['http://10.33.1.238:81',
                        'http://10.33.200.115:81', 'http://10.33.200.74:81', 'http://10.33.200.74:85']


# Application definition

INSTALLED_APPS = [
    'django_prometheus',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # =========== APLICACIONES DEL PROYECTO ===========
    'rest_framework',
    'rest_framework_simplejwt',  # PARA LA AUTENTICACIÓN POR MEDIO DE UN JSON WEB TOKEN
    'corsheaders',
    'USER_APP',
    'CATALOGOS',
    'DIGITALIZACION_APP',
    'DASHBOARD',
    
]

MIDDLEWARE = [
    #==========================metrics Prometheus================
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ==================== CORSHEADERS =====================
    'corsheaders.middleware.CorsMiddleware',
    # ==================== CORSHEADERS =====================
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alfresco_clone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alfresco_clone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uridec_dev',
        'USER': 'postgres',
        'PASSWORD': 'One0ne$1',
        'HOST': '10.33.21.168',
        'PORT': '5432',
    }
}


# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'postgres',
#        'USER': 'postgres',
#        'PASSWORD': 'Condusef01',
#        'HOST': '10.33.1.137',
#        'PORT': '5432',
#    }
# }


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

# ======================= AGREGAMOS ESTA LÍNEA PARA LA CONFIG DE NGINX  ==========================
STATIC_ROOT = '/static/'


# ======================= CONFIGURACIÓN PARA SUBIR DOCUMENTOS E IMÁGENES ==========================
MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'archexpedientes')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------DESACTIVAR CORSHEADERS----------------------------------
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    'http://10.33.1.238',
    'http://10.33.200.115',
    'http://10.33.200.74:81',
    'http://10.33.200.74:85'
]
# PRUEBa

X_FRAME_OPTIONS = 'SAMEORIGIN'
# X_FRAME_OPTIONS = 'ALLOWALL'


# X_FRAME_OPTIONS = 'ALLOW-FROM http://10.33.1.238'

MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB

# Configuración para archivos subidos
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
DEFAULT_FILE_STORAGE_OPTIONS = {'max_upload_size': MAX_UPLOAD_SIZE}


# -----------------------------MODIFICAR MODELO DE "USUARIO"----------------------------------
AUTH_USER_MODEL = 'USER_APP.User'


# -------------------------AUTENTICACIÓN POT MEDIO DE UN TOKEN-------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# ------MODIFICAR EL TIEMPO DE VIDA DEL "ACCESS TOKEN"

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    # Tiempo de vida de 4 horas
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=240),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),  # Tiempo de vida 3 días
    'BLACKLIST_AFTER_ROTATION': True,
}


# ======================= CONFIGURACION DE CELRY ======================
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER", "amqp://guest:guest@rabbitmq:5672/")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_BACKEND", "redis://redis:6379/0")
