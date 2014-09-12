SECRET_KEY = '1234'
INSTALLED_APPS = (
    'tests.default_app',
)
MIDDLEWARE_CLASSES = tuple()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SWAP = False
