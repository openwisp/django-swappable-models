from django.db import models
import swapper


class BaseType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Type(BaseType):
    class Meta:
        swappable = swapper.swappable_setting("default_app", "Type")


class Item(models.Model):
    type = models.ForeignKey(
        swapper.get_model_name('default_app', "Type"), on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
