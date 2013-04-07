# Django settings for weblarvae project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG


ADMINS = (
    ('Bruno Vellutini', 'organelas@gmail.com'),
)

MANAGERS = ADMINS

# Banco de dados local para desenvolvimento.
DATABASES = {
        'default': {
            'NAME': 'cebimar',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'nelas',
            'OPTIONS': {
                'autocommit': True,
                }
            }
        }

CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 3600,
            'OPTIONS': {
                'MAX_ENTRIES': 100000,
                }
            },
        'johnny': {
            'BACKEND': 'johnny.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'JOHNNY_CACHE': False,
            }
        }

JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_cifo'
DISABLE_QUERYSET_CACHE = True

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = 'cifo'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ufg4b4+q%jglrdb8*^yk4u#e-5t%8xf$lls&5zn0xn)nh18b%n'
