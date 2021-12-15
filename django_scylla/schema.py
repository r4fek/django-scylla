from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """
    This class and its subclasses are responsible for emitting schema-changing
    statements to the databases - model creation/removal/alteration, field
    renaming, index fiddling, and so on.
    """
    sql_create_table = "CREATE TABLE IF NOT EXISTS %(table)s (%(definition)s)"

    def skip_default(self, field):
        """ScyllaDB doesn't accept default values for columns"""
        return True

    def skip_default_on_alter(self, field):
        return True

    def column_sql(self, model, field, include_default=False):
        """
        Take a field and return its column definition.
        The field must already have had set_attributes_from_name() called.
        """
        # Get the column's type and use that as the basis of the SQL
        db_params = field.db_parameters(connection=self.connection)
        sql = db_params['type']
        params = []
        # Check for fields that aren't actually columns (e.g. M2M)
        if sql is None:
            return None, None
        if field.primary_key or field.unique:
            sql += " PRIMARY KEY"

        # Optionally add the tablespace if it's an implicitly indexed column
        tablespace = field.db_tablespace or model._meta.db_tablespace
        if tablespace and self.connection.features.supports_tablespaces and field.unique:
            sql += " %s" % self.connection.ops.tablespace_sql(tablespace, inline=True)
        # Return the sql
        return sql, params

    def add_constraint(self, model, constraint):
        return None  # TODO: fix it

    def alter_unique_together(self, model, old_unique_together, new_unique_together):
        return None
