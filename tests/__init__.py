import os

import django
from django.core.management import call_command
from django.test.utils import setup_test_environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
setup_test_environment()

django.setup()
call_command("makemigrations", "default_app", interactive=False)
if os.environ["DJANGO_SETTINGS_MODULE"] == "tests.swap_settings":
    call_command("makemigrations", "alt_app", interactive=False)
call_command("migrate", interactive=False)
