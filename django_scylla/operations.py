import calendar

from django.db.backends.base.operations import BaseDatabaseOperations


class DatabaseOperations(BaseDatabaseOperations):
    """
    Encapsulate backend-specific differences, such as the way a backend
    performs ordering or calculates the ID of a recently-inserted row.
    """

    compiler_module = "django_scylla.cql.compiler"

    def quote_name(self, name):
        """
        Return a quoted version of the given table, index, or column name. Do
        not quote the given name if it's already been quoted.
        """
        if name.startswith('"') and name.endswith('"'):
            return name
        return f'"{name}"'

    def prep_for_like_query(self, value):
        """Do no conversion, parent string-cast is SQL specific."""
        return value

    def prep_for_iexact_query(self, value):
        """Do no conversion, parent string-cast is SQL specific."""
        return value

    def adapt_datetimefield_value(self, value):
        """
        Convert `datetime.datetime` object to the 64-bit signed integer
        representing a number of milliseconds since the standard base time.
        @see more: https://docs.scylladb.com/getting-started/types/#working-with-timestamps
        """
        if value is None:
            return None
        ts = calendar.timegm(value.utctimetuple())
        return str(int(ts * 1e3 + getattr(value, "microsecond", 0) / 1e3))

    def bulk_insert_sql(self, fields, placeholder_rows):
        return " ".join("VALUES (%s)" % ", ".join(row) for row in placeholder_rows)

    def sql_flush(self, style, tables, *args, **kwargs):
        """
        Truncate all existing tables in current keyspace.
        :returns: an empty list
        """
        if tables:
            cql_list = []

            for table in tables:
                cql_list.append(f"TRUNCATE {table}")
            return cql_list
        return []

    def prepare_sql_script(self, sql):
        return [sql]
