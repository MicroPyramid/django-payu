import sys
import django
from django.conf import settings


if __name__ == "__main__":
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': './db.sqlite3'
            }
        },
        INSTALLED_APPS=['payu'],
    )
    django.setup()
    if sys.argv:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
