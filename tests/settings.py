from os import path

from cassandra import ConsistencyLevel

DEBUG = True
TEMPLATE_DEBUG = True
USE_TZ = True

ALLOWED_HOSTS = [ "*" ]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = (
    "demo",
    "django_scylla",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

DATABASES = {
    "default": {
        "ENGINE": "django_scylla",
        "HOST": "scylla",
        "PORT": 9042,
        "NAME": "testdb",
        "OPTIONS": {
            "replication": {
                "class": "SimpleStrategy",
                "replication_factor": 1
            },
            "connection": {
                "consistency_level": ConsistencyLevel.ONE
            },
            "execution_profile": {
                "request_timeout": 5,
            }
        },
    },
}

MIDDLEWARE = [
    # default django middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

PROJECT_DIR = path.abspath(path.join(path.dirname(__file__)))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
            ]
        },
    }
]

STATIC_URL = "/static/"

SECRET_KEY = "secret"  # noqa: S105

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "propagate": True, "level": "DEBUG"},
        # 'django': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'WARNING',
        # },
    },
}

ROOT_URLCONF = "tests.urls"

if not DEBUG:
    raise Exception("This settings file can only be used with DEBUG=True")
