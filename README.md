Swapper
=======

[![Dependency monitoring](https://img.shields.io/librariesio/release/github/openwisp/django-swappable-models)](https://libraries.io/github/openwisp/django-swappable-models)

#### Django Swappable Models - No longer only for auth.User!

Swapper is an unofficial API for the [undocumented] but very powerful Django 
feature: swappable models.  Swapper facilitates implementing
arbitrary swappable models in your own reusable apps.

[![Latest PyPI Release](https://img.shields.io/pypi/v/swapper.svg)](https://pypi.org/project/swapper)
[![Release Notes](https://img.shields.io/github/release/openwisp/django-swappable-models.svg
)](https://github.com/wq/django-swappable-models/releases)
[![License](https://img.shields.io/pypi/l/swapper.svg)](https://github.com/openwisp/django-swappable-models/blob/master/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/openwisp/django-swappable-models.svg)](https://github.com/openwisp/django-swappable-models/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/openwisp/django-swappable-models.svg)](https://github.com/openwisp/django-swappable-models/network)
[![GitHub Issues](https://img.shields.io/github/issues/openwisp/django-swappable-models.svg)](https://github.com/openwisp/django-swappable-models/issues)

[![Build Status](https://github.com/openwisp/django-swappable-models/actions/workflows/ci.yml/badge.svg)](https://github.com/openwisp/django-swappable-models/actions/workflows/ci.yml)
[![Python Support](https://img.shields.io/pypi/pyversions/swapper.svg)](https://pypi.org/project/swapper)
[![Django Support](https://img.shields.io/pypi/djversions/swapper.svg)](https://pypi.org/project/swapper)

## Motivation

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
these models and supplement them with their own additional fields.  You could use
Abstract classes (e.g. `BaseParent` and `BaseChild`) for this, but then you
would either need to:

 1. Avoid putting the foreign key on `BaseChild` and tell the user they need to
    do it.
 2. Put the foreign key on `BaseChild`, but make `Parent` a concrete model that
    can't be swapped
 3. Use swappable models, together with `ForeignKeys` that read the swappable
    settings.

This third approach is taken by Django to facilitate [swapping the auth.User model]. The `auth.User` swappable code was implemented in a generic way that allows it to be used for any model.  Although this capability is currently [undocumented] while any remaining issues are being sorted out, it has proven to be very stable and useful in our experience.

Swapper is essentially a simple API wrapper around this existing functionality.  Note that Swapper is primarily a tool for library authors; users of your reusable app generally should not need to know about Swapper in order to use it.  (See the notes on [End User Documentation](#end-user-documentation) below.)

### Real-World Examples

Swapper is used extensively in several OpenWISP packages to facilitate customization and extension.  Notable examples include:

 * [openwisp-users]
 * [openwisp-controller]
 * [openwisp-radius]

The use of swapper in these packages promotes [Software Reusability][reusability], one of the core values of the OpenWISP project.

## Creating a Reusable App

First, make sure you have `swapper` installed.  If you are publishing your reusable app as a Python package, be sure to add `swapper` to your project's dependencies (e.g. `setup.py`) to ensure that users of your app don't have errors integrating it.

```bash
pip3 install swapper
```
Extending the above example, you might create two abstract base classes and corresponding default implementations:

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

### Loading Swapped Models

In your reusable views and other functions, always use the swapper instead of importing swappable models directly.  This is because you might not know whether the user of your app is using your default implementation or their own version.

```python
# reusableapp/views.py

# Might work, might not
# from .models import Parent

import swapper
Parent = swapper.load_model("reusableapp", "Parent")
Child = swapper.load_model("reusableapp", "Child")

def view(request, *args, **kwargs):
    qs = Parent.objects.all()
    # ...
```

> Note: `swapper.load_model()` is the general equivalent of [get_user_model()] and subject to the same constraints: e.g. it should not be used until after the model system has fully initialized.

### Migration Scripts
Swapper can also be used in migration scripts to facilitate dependency ordering and foreign key references.  To use this feature in your library, generate a migration script with `makemigrations` and make the following changes.  In general, users of your library should not need to make any similar changes to their own migration scripts.  The one exception is if you have multiple levels of swappable models with foreign keys pointing to each other.

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
>                 'swappable': swapper.swappable_setting('reusableapp', 'Parent'),
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

## End User Documentation
With the above setup, the user of your app can override one or both models in their own app.  You might provide them with an example like this:

```python
# myapp/models.py
from reusableapp.models import BaseParent
class Parent(BaseParent):
    # custom implementation ...
```

Then, tell your users to update their settings to trigger the swap.

```python
# myproject/settings.py
REUSABLEAPP_PARENT_MODEL = "myapp.Parent"
```

The goal is to make this process just as easy for your end user as [swapping the auth.User model] is.  As with `auth.User`, there are some important caveats that you may want to inform your users about.

The biggest issue is that your users will probably need to define the swapped model settings **before creating any migrations** for their implementation of `myapp`.  Due to key assumptions made within Django's migration infrastructure, it is difficult to start out with a default (non-swapped) model and then later to switch to a swapped implementation without doing some migration hacking.  This is somewhat awkward - as your users will most likely want to try out your default implementation before deciding to customize it.  Unfortunately, there isn't an easy workaround due to how the swappable setting is currently implemented in Django core.  This will likely be addressed in future Django versions (see [#10] and [Django ticket #25313]).

## API Documentation

Here is the full API for `swapper`, which you may find useful in creating your reusable app code.  End users of your library should generally not need to reference this API.

function | purpose
---------|--------
`swappable_setting(app_label, model)` | Generates a swappable setting name for the provided model (e.g. `"REUSABLEAPP_PARENT_MODEL"`)
`is_swapped(app_label, model)` | Determines whether or not a given model has been swapped.  (Returns the model name if swapped, otherwise `False`)
`get_model_name(app_label, model)` | Gets the name of the model the swappable model has been swapped for (or the name of the original model if not swapped.)
`get_model_names(app_label, models)` | Match a list of model names to their swapped versions.  All of the models should be from the same app (though their swapped versions need not be).
`load_model(app_label, model, required=True)` | Load the swapped model class for a swappable model (or the original model if it hasn't been swapped).  If your code can function without the specified model, set `required = False`.
`dependency(app_label, model, version=None)` | Generate a dependency tuple for use in migrations. Use `version` only when depending on the first migration of the target dependency doesn't work (eg: when a specific migration needs to be depended upon), we recommend avoid using `version='__latest__'` because it can have serious [drawbacks] when new migrations are added to the module which is being depended upon.
`set_app_prefix(app_label, prefix)` | Set a custom prefix for swappable settings (the default is the upper case `app_label`).  This can be useful if the app has a long name or is part of a larger framework.  This should be set at the top of your models.py.
`join(app_label, model)`, `split(model)` | Utilities for splitting and joining `"app.Model"` strings and `("app", "Model")` tuples.

[undocumented]: https://code.djangoproject.com/ticket/19103
[swapping the auth.User model]: https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#auth-custom-user
[openwisp-users]: https://github.com/openwisp/openwisp-users#extend-openwisp-users
[openwisp-controller]: https://github.com/openwisp/openwisp-controller#extending-openwisp-controller
[openwisp-radius]: https://openwisp-radius.readthedocs.io/en/latest/developer/how_to_extend.html
[reusability]: https://openwisp.io/docs/general/values.html#software-reusability-means-long-term-sustainability
[get_user_model()]: https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#referencing-the-user-model
[#10]: https://github.com/openwisp/django-swappable-models/issues/10
[Django ticket #25313]: https://code.djangoproject.com/ticket/25313
[drawbacks]: https://code.djangoproject.com/ticket/23071
