from .settings import (  # noqa
    SECRET_KEY,
    INSTALLED_APPS,
    MIDDLEWARE_CLASSES,
    DATABASES,
)
INSTALLED_APPS += ('tests.alt_app',)
DEFAULT_APP_TYPE_MODEL = "alt_app.Type"
SWAP = True
