import os
import django
import pytest

os.environ['DJANGO_SETTINGS_MODULE'] = 'GestionEmpleados.settings'
django.setup()

pytestmark = pytest.mark.django_db
