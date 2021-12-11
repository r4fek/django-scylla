from cassandra.connection import Connection as Database
from django.db.backends.base.base import BaseDatabaseWrapper

from .client import DatabaseClient
from .creation import DatabaseCreation
from .features import DatabaseFeatures
from .introspection import DatabaseIntrospection
from .operations import DatabaseOperations
from .schema import DatabaseSchemaEditor
from .validation import DatabaseValidation


class DatabaseWrapper(BaseDatabaseWrapper):
    """Represent a database connection."""

    vendor = "scylladb"
    display_name = "ScyllaDB"

    # Mapping of Field objects to their column types.
    data_types = {
        "AutoField": "uuid",
        "BigAutoField": "uuid",
        "BinaryField": "blob",
        "BooleanField": "boolean",
        "CharField": "varchar(%(max_length)s)",
        "DateField": "date",
        "DateTimeField": "time",
        "DecimalField": "decimal",
        "DurationField": "duration",
        "FileField": "varchar(%(max_length)s)",
        "FilePathField": "varchar(%(max_length)s)",
        "FloatField": "float",
        "IntegerField": "int",
        "BigIntegerField": "bigint",
        "IPAddressField": "inet",
        "GenericIPAddressField": "inet",
        "JSONField": "text",
        "OneToOneField": "bigint",
        "PositiveBigIntegerField": "bigint",
        "PositiveIntegerField": "int",
        "PositiveSmallIntegerField": "tinyint",
        "SlugField": "varchar(%(max_length)s)",
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
