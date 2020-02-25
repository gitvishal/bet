"""
Django settings for bet project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2_@jskt2_27voo@_*5^^=ciy17c76@9%e#(7@u^wtqs*0c*^-o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

THIRDPARTY_PRIOR_APPS = [
	'django.contrib.sites',  
	'django.contrib.contenttypes',
	'grappelli.dashboard',
	'grappelli',
	'registration',
]

THIRDPARTY_APPS = [
	'bootstrap4', 
	'django_extensions',
	'ckeditor', 
	'phonenumber_field', 
	'easy_thumbnails',
	'django_countries',
	'simple_history',
	'mptt',
	'qr_code',
	'crispy_forms',
	'widget_tweaks',
]

BETTING_APPS = ['master', 'games',  'payments', ]

DJANGO_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

INSTALLED_APPS = THIRDPARTY_PRIOR_APPS + DJANGO_APPS + THIRDPARTY_APPS + BETTING_APPS

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'bet.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'bet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

from pytz import timezone as indiantime
INDIAN_TIME_ZONE = indiantime('Asia/Kolkata')
TIME_ZONE = INDIAN_TIME_ZONE.zone

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_URL = '/media/'

MEDIA_ROOT = os.path.join(os.environ['HOME'], 'storage', 'bet','media')
STATIC_ROOT = os.path.join(os.environ['HOME'], 'storage', 'bet','static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "bet", "static"), )

AUTH_USER_MODEL = "master.User"
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.

SITE_ID = 1


CKEDITOR_CONFIGS = {
	'default':{
		'skin': 'moono-lisa',
		'toolbar_Basic': [
			['Source', 'Bold', 'Italic']
		],
		'toolbar_Full': [
			['Font', 'FontSize', 'Format', 'Bold', 'Italic', 'Underline','Undo', 'Redo'],
			['NumberedList', 'BulletedList', 'Indent', 'Outdent',
				'JustifyLeft', 'JustifyCenter', 'JustifyRight','JustifyBlock'],
			['Link', 'Unlink',],
			['TextColor', 'BGColor','Image','Scayt'],
		],
		'toolbar': 'Full',
		'height': 291,
		'width': 700,

	},
}

THUMBNAIL_ALIASES = {
	'': {
		'avatar': {'size': (500, 500), 'crop': True},
	},
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'saugamya.goa@gmail.com'
EMAIL_HOST_PASSWORD = 'Vish@l%2143'
DEFAULT_FROM_EMAIL = 'saugamya.goa@gmail.com'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #thhis is for testing remove on prod move
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

##CRISPY FORM
CRISPY_TEMPLATE_PACK = 'bootstrap4'

##### Admin Configuration 				
GRAPPELLI_ADMIN_TITLE = 'Betting'                                  						
GRAPPELLI_INDEX_DASHBOARD = 'bet.dashboard.CustomIndexDashboard'

#phone
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'IN'
