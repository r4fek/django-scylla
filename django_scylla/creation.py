import sys

from django.db.backends.base.creation import BaseDatabaseCreation


class DatabaseCreation(BaseDatabaseCreation):
    """
    Encapsulate backend-specific differences pertaining to creation and
    destruction of the test database.
    """

    def _execute_create_test_db(self, cursor, parameters, keepdb=False):
        cursor.execute(
            "CREATE KEYSPACE %(dbname)s WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}"
            % parameters,
        )

    def _destroy_test_db(self, test_database_name, verbosity):
        with self._nodb_cursor() as cursor:
            cursor.execute(
                "DROP KEYSPACE %s" % self.connection.ops.quote_name(test_database_name)
            )

    def _create_test_db(self, verbosity, autoclobber, keepdb=False):
        """Create the test db tables."""
        test_database_name = self._get_test_db_name()
        test_db_params = {
            "dbname": self.connection.ops.quote_name(test_database_name),
            "suffix": self.sql_table_creation_suffix(),
        }
        # Create the test database and connect to it.
        with self._nodb_cursor() as cursor:
            try:
                self._execute_create_test_db(cursor, test_db_params, keepdb)
            except Exception as e:
                # if we want to keep the db, then no need to do any of the below,
                # just return and skip it all.
                if keepdb:
                    return test_database_name

                self.log("Got an error creating the test database: %s" % e)
                if not autoclobber:
                    confirm = input(
                        "Type 'yes' if you would like to try deleting the test "
                        "database '%s', or 'no' to cancel: " % test_database_name
                    )
                if autoclobber or confirm == "yes":
                    try:
                        if verbosity >= 1:
                            self.log(
                                "Destroying old test database for alias %s..."
                                % (
                                    self._get_database_display_str(
                                        verbosity, test_database_name
                                    ),
                                )
                            )
                        cursor.execute("DROP KEYSPACE %(dbname)s" % test_db_params)
                        self._execute_create_test_db(cursor, test_db_params, keepdb)
                    except Exception as e:
                        self.log("Got an error recreating the test database: %s" % e)
                        sys.exit(2)
                else:
                    self.log("Tests cancelled.")
                    sys.exit(1)

        return test_database_name
