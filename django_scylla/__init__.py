# monkey patch django.db.models.expressions
from django_scylla.cql.expressions import *  # noqa: F401, F403
from django_scylla.cql.query import *  # noqa: F401, F403
