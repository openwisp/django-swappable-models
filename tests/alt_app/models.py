from django.db import models
from tests.default_app.models import BaseType


class Type(BaseType):
    code = models.SlugField()

    class Meta:
        app_label = 'alt_app'
