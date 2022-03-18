from django.db.backends.base.introspection import BaseDatabaseIntrospection, TableInfo


class DatabaseIntrospection(BaseDatabaseIntrospection):
    """Encapsulate backend-specific introspection utilities."""

    def get_table_list(self, cursor):
        """Return a list of table and Materialized Views names in the current database"""
        keyspace = cursor.keyspace

        return [
            TableInfo(c[0], "t")
            for c in cursor.execute(
                "SELECT table_name FROM system_schema.tables WHERE keyspace_name=%s",
                params=(keyspace,),
            )
        ]
