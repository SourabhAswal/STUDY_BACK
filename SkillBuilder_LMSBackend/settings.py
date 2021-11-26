"""
Django settings for SkillBuilder_LMSBackend project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
# from google.cloud import storage

# client = storage.Client.from_service_account_json('/home/harshroxxx/Downloads/CREDENTIALS.json')
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/harshroxxx/Downloads/CREDENTIALS.json"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=t0p8s9at*h6_y_-(o@-r!%=(v2w$p)54tpx@9arv#9xeipi@2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # CORS
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'channels',
    'userauthn',
    'course',
    'discussion',
    'Super_Admin',
    'quizquestion',
    'assignment',
    'Studygroup_User',
    'Studygroup_SuperAdmin'
    
]

SITE_ID = 1

MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SkillBuilder_LMSBackend.urls'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/' # 'http://myhost:port/media/'

STATICFILES_DIRS=(
    os.path.join(BASE_DIR, 'static'),

)

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

# WSGI_APPLICATION = 'SkillBuilder_LMSBackend.wsgi.application'
ASGI_APPLICATION = 'SkillBuilder_LMSBackend.asgi.application'   

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("34.93.22.69", 6379)],
        },
    },
}

DATABASES = {
    'default': {

       'ENGINE': 'django.db.backends.mysql',
      
      
        'NAME': 'skillhub',# RCZ-GCP
        'USER': 'rishabh',
        'PASSWORD': 'Megha@00',
        'HOST': '35.244.54.102',

        'PORT': '3306',
    }
    
     
    
    
}

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': 'SECRET_KEY',
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}

CORS_ALLOW_ALL_ORIGINS = True
AUTH_USER_MODEL = 'userauthn.CustomUser'
TWILIO_ACCOUNT_SID = 'ACc0e9b213eda528614a7916084a689e44'
TWILIO_AUTH_TOKEN = '441ea43716dcb984a5c200ab684e53f5'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER ='jaiarora5080@gmail.com'
EMAIL_HOST_PASSWORD = 'fcyyonzxgoeqdnfk'
APPLICATION_EMAIL = 'Study Group<jaiarora5080@gmail.com>'
DEFAULT_FROM_EMAIL = 'Admindeafjut<jaiarora5080@gmail.com>'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER ='vipul1398@gmail.com'
# EMAIL_HOST_PASSWORD = 'zqzbmsqkaogzrnmk'
GOOGLE_CLOUD_STORAGE_URL='https://storage.googleapis.com/skillbuilder/'
GOOGLE_CLOUD_STORAGE_BUCKET='skillbuilder'
