from django.db.backends.base.introspection import BaseDatabaseIntrospection


class DatabaseIntrospection(BaseDatabaseIntrospection):
    """Encapsulate backend-specific introspection utilities."""
