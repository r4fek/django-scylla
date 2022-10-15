from django.apps import AppConfig


class DjangoScyllaAppConfig(AppConfig):
    name = "django_scylla"

    def ready(self):
        ...
