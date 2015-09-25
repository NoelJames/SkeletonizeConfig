from configparser import ConfigParser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# create and configure `local.settings.ini` with sensitive information
local_settings_ini = os.path.join(BASE_DIR, 'local.settings.ini')
config = ConfigParser()
config.read(local_settings_ini)

config.getfloat('foo', 'float_name')
config.getint('foo', 'int_name')

SECRET_KEY = config.get('secrets', 'key')
DEBUG = config.getboolean('debug', 'debug')
INTERNAL_IPS = tuple(config.get('debug', 'internal_ips').split())
ALLOWED_HOSTS = tuple(config.get('debug', 'internal_ips').split())

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'engine'),
        'NAME': config.get('database', 'name'),
        'USER': config.get('database', 'user'),
        'PASSWORD': config.get('database', 'password'),
        'HOST': config.get('database', 'host'),
        'PORT': config.get('database', 'port')
    }
}

# email
EMAIL_HOST_USER = config.get('email', 'user')
EMAIL_HOST_PASSWORD = config.get('email', 'password')
EMAIL_HOST = config.get('email', 'host')
EMAIL_PORT = config.get('email', 'port')
EMAIL_USE_TLS = config.getboolean('email', 'use_tls')
DEFAULT_FROM_EMAIL = config.get('email', 'default_from')

# Server settings
BASE_URL = config.get('server', 'base_url')
