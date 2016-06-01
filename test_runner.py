import sys
import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["payu"])
    sys.exit(bool(failures))
