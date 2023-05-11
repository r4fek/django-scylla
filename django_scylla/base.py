import json

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import EXEC_PROFILE_DEFAULT, ExecutionProfile, ProtocolVersion
from cassandra.policies import RoundRobinPolicy, TokenAwarePolicy
from cassandra.query import tuple_factory
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
    DEFAULT_PROTOCOL_VERSION = ProtocolVersion.V4

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
        "PositiveSmallIntegerField": "smallint",
        "SlugField": "text",
        "SmallAutoField": "bigint",
        "SmallIntegerField": "smallint",
        "TextField": "text",
        "TimeField": "time",
        "UUIDField": "uuid"
    }

    operators = {
        "exact": "= %s",
        "iexact": "= %s",
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
        out_params = {}
        options = self.settings_dict.get("OPTIONS", {})

        connection_options = options.get("connection", {})
        replication_options = options.get("replication", {})
        execution_profile_options = options.get("execution_profile", {})

        if not replication_options.get("class"):
            raise ValueError(
                "Missing configuration value: OPTIONS.replication.class\n"
                "See: https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/architecture/archDataDistributeReplication.html"  # noqa
            )

        if not replication_options.get("replication_factor"):
            raise ValueError(
                "Missing configuration value: OPTIONS.replication.replication_factor\n"
                "See: https://docs.datastax.com/en/cql-oss/3.3/cql/cql_using/useUpdateKeyspaceRF.html"
            )

        ep_keys = (
            "load_balancing_policy",
            "retry_policy",
            "consistency_level",
            "serial_consistency_level",
            "request_timeout",
            "speculative_execution_policy",
        )

        if not connection_options.get("contact_points"):
            out_params["contact_points"] = self.settings_dict["HOST"].split(",")
        if not connection_options.get("port") and self.settings_dict.get("PORT"):
            out_params["port"] = int(self.settings_dict["PORT"])
        if connection_options.get("auth_provider") is None and (
            self.settings_dict.get("USER") and self.settings_dict.get("PASSWORD")
        ):
            out_params["auth_provider"] = PlainTextAuthProvider(
                username=self.settings_dict["USER"],
                password=self.settings_dict["PASSWORD"],
            )
        if connection_options.get("protocol_version") is None:
            out_params["protocol_version"] = self.DEFAULT_PROTOCOL_VERSION

        ep_options = {
            k: execution_profile_options.pop(k, None)
            for k in ep_keys
            if execution_profile_options.get(k)
        }
        ep_options["row_factory"] = tuple_factory
        if "load_balancing_policy" not in ep_options:
            ep_options["load_balancing_policy"] = TokenAwarePolicy(RoundRobinPolicy())

        out_params["execution_profiles"] = {
            EXEC_PROFILE_DEFAULT: ExecutionProfile(**ep_options)
        }
        return out_params

    def get_new_connection(self, conn_params):
        """Open a connection to the database."""
        db = self.settings_dict["NAME"]
        cluster = Database.initialize(db, **conn_params)

        cursor = Cursor(cluster.connect())

        # Ensure that the keyspace exists before using it, if possible.
        if db is not None:
            replication_options = json.dumps(
                self.settings_dict["OPTIONS"]["replication"]
            ).replace('"', "'")

            cursor.execute(
                (
                    "CREATE KEYSPACE IF NOT EXISTS {db} "
                    "WITH REPLICATION = {replication}".format(
                        db=db, replication=replication_options
                    )
                )
            )

        return cursor

    def init_connection_state(self):
        """Initialize the database connection settings."""
        ...

    def create_cursor(self, name=None):
        """Create a cursor. Assume that a connection is established."""
        name = name or self.settings_dict["NAME"]
        if name is not None:
            self.connection.set_keyspace(name)
        return self.connection

    def _set_autocommit(self, autocommit):
        ...

    def _commit(self):
        ...

    def _rollback(self):
        ...
