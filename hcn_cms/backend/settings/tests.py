from .settings import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['PG_DATABASE'],
        'USER': os.environ['PG_USER'],
        'PASSWORD': os.environ['PG_PASSWORD'],
        'HOST': '127.0.0.1',  # os.environ['PG_HOST'],
        'PORT': '5432',
    }
}
