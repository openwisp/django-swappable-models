import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "tests.settings")

from django.test.utils import setup_test_environment
setup_test_environment()

from django.core.management import call_command

import django
if hasattr(django, 'setup'):
    # Django 1.7+
    django.setup()
    call_command('makemigrations', 'default_app', interactive=False)
    if os.environ["DJANGO_SETTINGS_MODULE"] == "tests.swap_settings":
        call_command('makemigrations', 'alt_app', interactive=False)
    call_command('migrate', interactive=False)
else:
    # Django 1.6
    call_command('syncdb', interactive=False)
