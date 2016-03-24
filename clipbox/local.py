from .common import *

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'video',
    'haystack',
    #'easy_thumbnails',
    'sorl.thumbnail',
    'social.apps.django_app.default',
)


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
#}


#removed when moving to heroku
DATABASES = {  
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'framedb2',                      # Or path to database file if using sqlite3.
		'USER': 'postgres',                      # Not used with sqlite3.
		'PASSWORD': 'JONES2678',                  # Not used with sqlite3.
		'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
	}
}




STATIC_ROOT = os.path.join(ENV_PATH, 'static/')
STATIC_URL = '/static/'

STATICFILES_LOCATION = 'static'

#Tell the staticfiles app to use S3Boto storage when writing the collected static files (when you run `collectstatic`).
#turn this line on when collecting static for online!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#STATICFILES_STORAGE = 'custom_storages.StaticStorage'

