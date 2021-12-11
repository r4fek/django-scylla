from django.db.backends.base.creation import BaseDatabaseCreation


class DatabaseCreation(BaseDatabaseCreation):
    """
    Encapsulate backend-specific differences pertaining to creation and
    destruction of the test database.
    """
