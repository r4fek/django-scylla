from django.db.backends.base.operations import BaseDatabaseOperations


class DatabaseOperations(BaseDatabaseOperations):
    """
    Encapsulate backend-specific differences, such as the way a backend
    performs ordering or calculates the ID of a recently-inserted row.
    """
