from django.db.backends.base.introspection import BaseDatabaseIntrospection, TableInfo


class DatabaseIntrospection(BaseDatabaseIntrospection):
    """Encapsulate backend-specific introspection utilities."""

    def get_table_list(self, cursor):
        """Return a list of table and Materialized Views names in the current database"""
        keyspace = cursor.keyspace

        return [
            TableInfo(c, 't') for c in cursor.execute(
                f"select table_name from system_schema.tables where keyspace_name='{keyspace}'")
        ]
