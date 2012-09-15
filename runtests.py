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

log_sql = False
if '--log-sql' in sys.argv:
    log_sql = True
    sys.argv.remove('--log-sql')

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
        DEBUG = log_sql,
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
            },
            'formatters': {
                'simple': {
                    'format': '%(levelname)s %(message)s',
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                },
            },
        } if log_sql else {},
    )

    if log_sql:
        from django.db import connection
        connection.use_debug_cursor = True

        # Django won't configure for us!
        from logging.config import dictConfig
        dictConfig(settings.LOGGING)

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
