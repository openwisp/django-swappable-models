Swapper
=======

#### Django Swappable Models - No longer only for auth.User!

Swapper is an unofficial API for the [undocumented] but very powerful Django 
feature: swappable models.  Swapper facilitates implementing
arbitrary swappable models in your own reusable apps.

[![Build Status](https://travis-ci.org/wq/django-swappable-models.svg?branch=master)](https://travis-ci.org/wq/django-swappable-models)
[![PyPI Package](https://pypip.in/version/swapper/badge.png)](https://pypi.python.org/pypi/swapper)

Tested on Python 2.7 and 3.4, with Django 1.6 and 1.7.

## Example Use Case

Suppose your reusable app has two related tables:

```python
from django.db import models
class Parent(models.Model):
    name = models.TextField()

class Child(models.Model):
    name = models.TextField()
    parent = models.ForeignKey(Parent)
```

Suppose further that you want to allow the user to subclass either or both of
these models and supplement them with their own implementations.  You could use
Abstract classes (e.g. `BaseParent` and `BaseChild`) for this, but then you
would either need to:

 1. Avoid putting the foreign key on `BaseChild` and tell the user they need to
    do it.
 2. Put the foreign key on `BaseChild`, but make `Parent` a concrete model that
    can't be swapped
 3. Use swappable models, together with `ForeignKeys` that read the swappable
    settings.

This third approach is taken by Django to facilitate [swapping the auth.User
model].  Swapper extends this approach to apply to any model.

## Real-World Example
Swapper is used extensively in the [vera] extension to [wq.db].  vera provides [7 inter-related models], each of which can be swapped out for custom implementations.  (Swapper actually started out as part of [wq.db.patterns], but was extracted for more general-purpose use.)

## Getting Started

```bash
pip3 install swapper
```

## Usage

Extending the above example, create abstract base classes and default 
implementations:

```python
# reusableapp/models.py
from django.db import models
import swapper

class BaseParent(models.Model):
    # minimal base implementation ...
    class Meta:
        abstract = True

class Parent(BaseParent):
    # default (swappable) implementation ...
    class Meta:
       swappable = swapper.swappable_setting('reusableapp', 'Parent')

class BaseChild(models.Model):
    parent = models.ForeignKey(swapper.get_model_name('reusableapp', 'Parent'))
    # minimal base implementation ...
    class Meta:
        abstract = True

class Child(BaseChild):
    # default (swappable) implementation ...
    class Meta:
       swappable = swapper.swappable_setting('reusableapp', 'Child')
```

### User Customization
With the above setup, the user of your app can override one or both models in their own app:

```python
# myapp/models.py
from reusableapp.models import BaseParent
class Parent(BaseParent):
    # custom implementation ...
```

The user then specifies the appropriate setting to trigger the swap:

```python
# myproject/settings.py
REUSABLEAPP_PARENT_MODEL = "myapp.Parent"
```

### Loading Swapped Models

Note: Instead of importing concrete models directly, always use the swapper:

```python
# reusableapp/views.py

# Might work, might not
# from .models import Parent

import swapper
Parent = swapper.load_model("reusableapp", "Parent")
Child = swapper.load_model("reusableapp", "Parent")

def view(request, *args, **kwargs):
    qs = Parent.objects.all()
    # ...
```

### Migration Scripts
Swapper can also be used in Django 1.7+ migration scripts to facilitate dependency ordering and foreign key references.  To use this feature, generate a migration script with `makemigrations` and make the following changes: 

```diff
  # reusableapp/migrations/0001_initial.py

  from django.db import models, migrations
< from django.conf import settings
> import swapper

  class Migration(migrations.Migration):

      dependencies = [
<          migrations.swappable_dependency(settings.REUSABLEAPP_PARENT_MODEL),
>          swapper.dependency('reusableapp', 'Parent')
      ]

      operations = [
          migrations.CreateModel(
              name='Child',
              fields=[
                  ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
              ],
              options={
<                 'swappable': 'REUSABLEAPP_CHILD_MODEL',
>                 'swappable': swapper.swappable_setting('reusableapp', 'Child'),
              },
              bases=(models.Model,),
          ),
          migrations.CreateModel(
              name='Parent',
              fields=[
                  ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
              ],
              options={
<                 'swappable': 'REUSABLEAPP_PARENT_MODEL',
>                 'swappable': swapper.swappable_setting('reusableapp', 'Child'),
              },
              bases=(models.Model,),
          ),
          migrations.AddField(
              model_name='child',
              name='parent',
<             field=models.ForeignKey(to=settings.REUSABLEAPP_PARENT_MODEL),
>             field=models.ForeignKey(to=swapper.get_model_name('reusableapp', 'Parent')),
              preserve_default=True,
          ),
      ]
```

## API Documentation

function | purpose
---------|--------
`swappable_setting(app_label, model)` | Generates a swappable setting name for the provided model (e.g. `"REUSABLEAPP_PARENT_MODEL"`)
`is_swapped(app_label, model)` | Determines whether or not a given model has been swapped.  (Returns the model name if swapped, otherwise `False`)
`get_model_name(app_label, model)` | Gets the name of the model the swappable model has been swapped for (or the name of the original model if not swapped.)
`get_model_names(app_label, models)` | Match a list of model names to their swapped versions.  All of the models should be from the same app (though their swapped versions need not be).
`load_model(app_label, model, required=True)` | Load the swapped model class for a swappable model (or the original model if it hasn't been swapped).
`dependency(app_label, model)` | Generate a dependency tuple for use in Django 1.7+ migrations.
`set_app_prefix(app_label, prefix)` | Set a custom prefix for swappable settings (the default is the upper case `app_label`).  Used in [wq.db] to make all of the swappable settings start with `"WQ"` (e.g. `WQ_FILE_MODEL` instead of `FILES_FILE_MODEL`).  This should be set at the top of your models.py.
`join(app_label, model)`, `split(model)` | Utilities for splitting and joining `"app.Model"` strings and `("app", "Model")` tuples.

[undocumented]: https://code.djangoproject.com/ticket/19103
[swapping the auth.User model]: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-custom-user
[wq.db]: http://wq.io/wq.db
[vera]: http://wq.io/vera
[wq.db.patterns]: http://wq.io/docs/about-patterns
[7 inter-related models]: https://github.com/wq/vera/blob/master/vera/models.py
