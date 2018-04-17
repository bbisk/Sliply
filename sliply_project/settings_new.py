import environ
root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env() # reading .env file

SITE_ROOT = root()

DEBUG = env('DEBUG') # False if not in os.environ
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
}

public_root = root.path('')

MEDIA_ROOT = public_root('media')
MEDIA_URL = 'media/'
STATIC_ROOT = public_root('static')
STATIC_URL = 'static/'

SECRET_KEY = env('SECRET_KEY') # Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ

CACHES = {
    'default': env.cache(),
    'redis': env.cache('REDIS_URL')
}