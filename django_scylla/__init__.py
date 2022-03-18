# monkey patch django.db.models.expressions
from django_scylla.cql.expressions import *  # noqa: F401, F403
