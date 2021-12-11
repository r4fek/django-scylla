from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """
    This class and its subclasses are responsible for emitting schema-changing
    statements to the databases - model creation/removal/alteration, field
    renaming, index fiddling, and so on.
    """

    def skip_default(self, field):
        """ScyllaDB doesn't accept default values for columns"""
        return True

    def skip_default_on_alter(self, field):
        return True
