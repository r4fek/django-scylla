from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """
    This class and its subclasses are responsible for emitting schema-changing
    statements to the databases - model creation/removal/alteration, field
    renaming, index fiddling, and so on.
    """

    sql_create_table = "CREATE TABLE IF NOT EXISTS %(table)s (%(definition)s)"
    sql_create_index = "CREATE INDEX IF NOT EXISTS %(name)s ON %(table)s (%(columns)s)"
    sql_delete_column = "ALTER TABLE %(table)s DROP %(column)s"

    def skip_default(self, field):
        return False

    def skip_default_on_alter(self, field):
        return True

    def column_sql(self, model, field, include_default=False):
        """
        Take a field and return its column definition.
        The field must already have had set_attributes_from_name() called.
        """
        # Get the column's type and use that as the basis of the SQL
        db_params = field.db_parameters(connection=self.connection)
        sql = db_params["type"]
        params = []
        # Check for fields that aren't actually columns (e.g. M2M)
        if sql is None:
            return None, None
        if field.primary_key:
            sql += " PRIMARY KEY"

        # Optionally add the tablespace if it's an implicitly indexed column
        tablespace = field.db_tablespace or model._meta.db_tablespace
        if (
            tablespace
            and self.connection.features.supports_tablespaces
            and field.unique
        ):
            sql += " %s" % self.connection.ops.tablespace_sql(tablespace, inline=True)
        # Return the sql
        return sql, params

    def add_constraint(self, model, constraint):
        ...  # TODO: fix it

    def alter_unique_together(self, model, old_unique_together, new_unique_together):
        ...

    def alter_index_together(self, model, old_index_together, new_index_together):
        return None

    def _create_unique_sql(self, *args, **kwargs):
        # TODO: fix it
        return ""

    def _create_index_name(self, table_name, column_names, suffix=""):
        return f"{table_name}_by_{'_'.join(column_names)}"

    def _alter_column_null_sql(self, model, old_field, new_field):
        return ""
