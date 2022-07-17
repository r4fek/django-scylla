from cassandra.auth import PlainTextAuthProvider
from django.db.backends.base.base import BaseDatabaseWrapper

from . import database as Database
from .client import DatabaseClient
from .creation import DatabaseCreation
from .cursor import Cursor
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor
from .validation import DatabaseValidation


class DatabaseWrapper(BaseDatabaseWrapper):
    """Represent a database connection."""

    vendor = "scylladb"
    display_name = "ScyllaDB"
    DEFAULT_PROTOCOL_VERSION = 4

    # Mapping of Field objects to their column types.
    data_types = {
        "AutoField": "bigint",
        "BigAutoField": "bigint",
        "BinaryField": "blob",
        "BooleanField": "boolean",
        "CharField": "text",
        "DateField": "date",
        "DateTimeField": "timestamp",
        "DecimalField": "decimal",
        "DurationField": "duration",
        "FileField": "text",
        "FilePathField": "text",
        "FloatField": "float",
        "ForeignKeyField": "bigint",
        "IntegerField": "bigint",
        "BigIntegerField": "bigint",
        "IPAddressField": "inet",
        "GenericIPAddressField": "inet",
        "JSONField": "text",
        "ManyToOneRel": "bigint",
        "OneToOneField": "bigint",
        "PositiveBigIntegerField": "bigint",
        "PositiveIntegerField": "bigint",
        "PositiveSmallIntegerField": "tinyint",
        "RelatedField": "bigint",
        "SlugField": "text",
        "SmallAutoField": "int",
        "SmallIntegerField": "tinyint",
        "TextField": "text",
        "TimeField": "time",
        "UUIDField": "uuid",
    }

    operators = {
        "exact": "= %s",
        "contains": "CONTAINS %s",
        "gt": "> %s",
        "gte": ">= %s",
        "lt": "< %s",
        "lte": "<= %s",
    }

    Database = Database
    SchemaEditorClass = DatabaseSchemaEditor
    # Classes instantiated in __init__().
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    validation_class = DatabaseValidation

    queries_limit = 9000

    def get_connection_params(self):
        """Return a dict of parameters suitable for get_new_connection."""
        options = self.settings_dict.get("OPTIONS", {})

        if not options.get("contact_points"):
            options["contact_points"] = self.settings_dict["HOST"].split(",")
        if not options.get("port") and self.settings_dict.get("PORT"):
            options["port"] = int(self.settings_dict["PORT"])
        if options.get("auth_provider") is None and (
            self.settings_dict.get("USER") and self.settings_dict.get("PASSWORD")
        ):
            options["auth_provider"] = PlainTextAuthProvider(
                username=self.settings_dict["USER"],
                password=self.settings_dict["PASSWORD"],
            )
        if options.get("protocol_version") is None:
            options["protocol_version"] = self.DEFAULT_PROTOCOL_VERSION

        return options

    def get_new_connection(self, conn_params):
        """Open a connection to the database."""
        db = self.settings_dict["NAME"]
        cluster = Database.initialize(db, **conn_params)
        return Cursor(cluster.connect(db))

    def init_connection_state(self):
        """Initialize the database connection settings."""
        ...

    def create_cursor(self, name=None):
        """Create a cursor. Assume that a connection is established."""
        self.connection.set_keyspace(name or self.settings_dict["NAME"])
        return self.connection

    def _set_autocommit(self, autocommit):
        ...

    def _commit(self):
        ...

    def _rollback(self):
        ...
