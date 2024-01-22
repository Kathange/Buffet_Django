"""
Django settings for buffetProject project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%ia5a#mtwpv#3i5v*8%a(ud%g5h$#-s0#iq_d#_r*+6%db6$@6'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG設為True就可以在django發生錯誤的時候，將錯誤顯示在網頁上方，方便除蟲。
# 所以在正式的網站上，DEBUG 必須要設為False才比較安全。
DEBUG = True

ALLOWED_HOSTS = ['3.136.127.234', '127.0.0.1']

# AUTH_USER_MODEL = 'interface.user'

# # 檢查是否使用runserver命令
# if 'runserver' in sys.argv:
#     # 設定host和port
#     RUNSERVER_PORT = 8080  # 你想要使用的端口號
#     RUNSERVER_ADDR = '127.0.0.1'  # 你想要使用的主機地址
#     sys.argv = ['manage.py', 'runserver', f'{RUNSERVER_ADDR}:{RUNSERVER_PORT}'] + sys.argv[2:]


# Application definition

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 600  # 10 mins (in seconds)

INSTALLED_APPS = [
    'interface',    # 加入名為 interface 的app(資料夾)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
]

# # Ngrok安全性设置
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http,https')

ROOT_URLCONF = 'buffetProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 加入template (html相關) 設定
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'buffetProject.wsgi.application'

# AUTHENTICATION_BACKENDS = [
#     'buffetProject.custom_auth.CustomAuthBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': '3d_cafeteria',
#         'USER': 'root',
#         'PASSWORD': '1234',     # 我自己當初安裝時設的密碼
#         'HOST': 'localhost',
#         'PORT': 3306,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '3d_buffet',
        'USER': 'project',
        'PASSWORD': '3dbuffet',     # 我自己當初安裝時設的密碼
        'HOST': '3.136.127.234',
        'PORT': 3306,
        # 'OPTIONS': {
        #     'charset': 'utf8mb4',
        # },
    }
}

MIGRATION_MODULES = {
    'interface': None, 
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True

# Static files 靜態檔案的設定 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# DEBUG = True 時用
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
]
# DEBUG = False 時用
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # login logout 的設定(還未用到)
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'


# # 上傳 imgae 的設定
# MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'



