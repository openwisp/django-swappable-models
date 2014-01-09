from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


_prefixes = {}


def swappable_setting(app_label, model):
    """
    Returns the setting name to use for the given model (i.e. AUTH_USER_MODEL)
    """
    prefix = _prefixes.get(app_label, app_label)
    return "{prefix}_{model}_MODEL".format(
        prefix=prefix.upper(),
        model=model.upper()
    )


def is_swapped(app_label, model):
    """
    Returns the value of the swapped setting, or False if the model hasn't
    been swapped.
    """
    default_model = "%s.%s" % (app_label, model)
    setting = swappable_setting(app_label, model)
    value = getattr(settings, setting, default_model)
    if value != default_model:
        return value
    else:
        return False


def get_model_name(app_label, model):
    """
    Returns [app_label.model] unless the model has been swapped, in which case
    returns the swappable setting value.
    """
    return is_swapped(app_label, model) or join(app_label, model)


def get_model_names(app_label, models):
    """
    Map model names to their swapped equivalents for the given app
    """
    return {
        model: get_model_name(app_label, model)
        for model in models
    }


def load_model(app_label, model, orm=None, required=True):
    """
    Load the specified model class, or the class it was swapped out for.
    If a South orm object is provided, it will be used (but only if the
    model hasn't been swapped.)
    """
    swapped = is_swapped(app_label, model)
    if swapped:
        app_label, model = split(swapped)
    else:
        if orm is not None:
            return orm[join(app_label, model)]

    from django.db.models import get_model
    cls = get_model(app_label, model)
    if cls is None and required:
        raise ImproperlyConfigured(
            "Could not find {name}!".format(name=join(app_label, model))
        )
    return cls


def set_app_prefix(app_label, prefix):
    """
    Set a custom prefix to use for the given app (e.g. WQ)
    """
    _prefixes[app_label] = prefix


def join(app_label, model):
    return "{app_label}.{model}".format(
        app_label=app_label,
        model=model,
    )


def split(model):
    app_label, model = model.split(".")
    return app_label, model
