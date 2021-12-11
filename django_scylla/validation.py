from django.db.backends.base.validation import BaseDatabaseValidation


class DatabaseValidation(BaseDatabaseValidation):
    """Encapsulate backend-specific validation."""
