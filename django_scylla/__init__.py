# monkey patch django.db.models.expressions
from django.db.models.base import Model

from django_scylla.cql.expressions import *  # noqa: F401, F403
from django_scylla.cql.query import *  # noqa: F401, F403
from django_scylla.cql.where import *  # noqa: F401, F403


def maybe_validate_unique(self, exclude=None):
    if exclude:
        return
    else:
        return self.validate_unique()

Model.validate_unique = maybe_validate_unique
