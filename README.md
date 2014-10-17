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

## Getting Started

```bash
pip install swapper
```

## Usage

Extending the above example, create abstract base classes and default 
implementations:

```python
# reusableapp/models.py
from django.db import models
from swapper import swappable_setting, get_model_name

class BaseParent(models.Model):
    # minimal base implementation ...
    class Meta:
        abstract = True

class Parent(BaseParent):
    # default (swappable) implementation ...
    class Meta:
       swappable = swappable_setting('reusableapp', 'Parent')

class BaseChild(models.Model):
    parent = models.ForeignKey(get_model_name('reusableapp', 'Parent'))
    # minimal base implementation ...
    class Meta:
        abstract = True

class Child(BaseChild):
    # default (swappable) implementation ...
    class Meta:
       swappable = swappable_setting('reusableapp', 'Child')
```

Then the user can override one or both models in their own app:

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

Note: Instead of importing concrete models directly, always use the swapper:

```python
# reusableapp/views.py

# Might work, might not
# from .models import Parent

from swapper import load_model
Parent = load_model("reusableapp", "Parent")
Child = load_model("reusableapp", "Parent")

def view(request, *args, **kwargs):
    qs = Parent.objects.all()
    # ...
```

## Real-World Example
Swapper is used extensively in the [vera] extension to [wq.db].  vera provides [7 inter-related models], each of which can be swapped out for custom implementations.  (Swapper actually started out as part of [wq.db.patterns], but was extracted for more general-purpose use.)

[undocumented]: https://code.djangoproject.com/ticket/19103
[swapping the auth.User model]: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-custom-user
[wq.db]: http://wq.io/wq.db
[vera]: http://wq.io/vera
[wq.db.patterns]: http://wq.io/docs/about-patterns
[7 inter-related models]: https://github.com/wq/wq.db/blob/master/contrib/vera/models.py
