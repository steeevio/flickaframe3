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
    'gunicorn',
    'haystack',
    #'easy_thumbnails',
    'sorl.thumbnail',
    'social.apps.django_app.default',
)


DATABASES = {
    'default': dj_database_url.config()
}

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.

#STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#using defined classes to seperate media and static on S3
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
