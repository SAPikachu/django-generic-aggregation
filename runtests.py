#!/usr/bin/env python
import sys
from os.path import dirname, abspath

from django.conf import settings

if len(sys.argv) > 1 and 'postgres' in sys.argv:
    sys.argv.remove('postgres')
    db_engine = 'django.db.backends.postgresql_psycopg2'
    db_name = 'test_main'
else:
    db_engine = 'django.db.backends.sqlite3'
    db_name = ''

if not settings.configured:
    settings.configure(
        DATABASES = {
            "default": {
                "ENGINE": db_engine,
                "NAME": db_name,
            },
        },
        INSTALLED_APPS = [
            'django.contrib.contenttypes',
            'generic_aggregation.generic_aggregation_tests',
        ],
    )

from django.test.utils import get_runner

def runtests(*test_args):
    if not test_args:
        test_args = ['generic_aggregation_tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    Runner = get_runner(settings)
    failures = Runner(verbosity=1, interactive=True).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
