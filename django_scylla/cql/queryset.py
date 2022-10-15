from django.db import NotSupportedError
from django.db.models.query import QuerySet


def patched_exclude(self, *args, **kwargs):
    raise NotSupportedError("Calling QuerySet.exclude() is not supported yet.")


QuerySet.exclude = patched_exclude
