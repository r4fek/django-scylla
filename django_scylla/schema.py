import logging

from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from django_scylla.constraints import PrimaryKeysConstraint

logger = logging.getLogger(__name__)


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    """
    This class and its subclasses are responsible for emitting schema-changing
    statements to the databases - model creation/removal/alteration, field
    renaming, index fiddling, and so on.
    """

    sql_create_column = "ALTER TABLE %(table)s ADD %(column)s %(definition)s"
    sql_create_table = "CREATE TABLE IF NOT EXISTS %(table)s (%(definition)s)"
    sql_create_index = "CREATE INDEX IF NOT EXISTS %(name)s ON %(table)s (%(columns)s)"
    sql_delete_column = "ALTER TABLE %(table)s DROP %(column)s"
    sql_create_primary_keys = "PRIMARY KEY %(columns)s"

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

        return sql, params

    def table_sql(self, model):
        """Add primary key definitions"""
        # check if PrimaryKeysConstraint is present in model._meta
        for constraint in model._meta.constraints:
            if isinstance(constraint, PrimaryKeysConstraint):
                return super().table_sql(model)

        # No manually added PrimaryKeysConstraint in meta. Creating then!
        pk_fields = [f.column for f in model._meta.fields if f.primary_key]
        model._meta.constraints.append(PrimaryKeysConstraint(fields=pk_fields))
        sql, params = super().table_sql(model)
        logger.debug("table_sql %s, params %s", sql, params)
        return sql, params

    def _create_primary_keys_sql(self, fields):
        if len(fields) == 1:
            columns = f'("{fields[0]}")'
        else:
            columns = str(fields).replace("'", '"')
        return self.sql_create_primary_keys % {"columns": columns}

    def add_constraint(self, model, constraint):
        logger.debug("add_constraint %s", constraint)
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
