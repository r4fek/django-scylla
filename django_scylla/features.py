from django.db.backends.base.features import BaseDatabaseFeatures


class DatabaseFeatures(BaseDatabaseFeatures):
    allows_group_by_lob = False
    update_can_self_select = False

    can_use_chunked_reads = True
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False
    has_bulk_insert = False
    has_select_for_update = False
    uses_savepoints = False
    can_release_savepoints = False

    supports_subqueries_in_group_by = False

    # If True, don't use integer foreign keys referring to, e.g., positive
    # integer primary keys.
    related_fields_match_type = True

    # Does the backend ignore unnecessary ORDER BY clauses in subqueries?
    ignores_unnecessary_order_by_in_subqueries = True

    # Is there a true datatype for uuid?
    has_native_uuid_field = True

    # Is there a true datatype for timedeltas?
    has_native_duration_field = True

    # Does the database driver supports same type temporal data subtraction
    # by returning the type used to store duration field?
    supports_temporal_subtraction = False

    # Does the __regex lookup support backreferencing and grouping?
    supports_regex_backreferencing = False

    # Can date/datetime lookups be performed using a string?
    supports_date_lookup_using_string = True

    # Can datetimes with timezones be used?
    supports_timezones = True

    # Does the database have a copy of the zoneinfo database?
    has_zoneinfo_database = True

    # When performing a GROUP BY, is an ORDER BY NULL required
    # to remove any ordering?
    requires_explicit_null_ordering_when_grouping = False

    # Does the backend order NULL values as largest or smallest?
    nulls_order_largest = False

    # Does the backend support NULLS FIRST and NULLS LAST in ORDER BY?
    supports_order_by_nulls_modifier = False

    # Does the backend orders NULLS FIRST by default?
    order_by_nulls_first = False

    # The database's limit on the number of query parameters.
    max_query_params = None

    # Can an object have an autoincrement primary key of 0?
    allows_auto_pk_0 = True

    # Do we need to NULL a ForeignKey out, or can the constraint check be
    # deferred
    can_defer_constraint_checks = False

    # date_interval_sql can properly handle mixed Date/DateTime fields and timedeltas
    supports_mixed_date_datetime_comparisons = True

    # Does the backend support tablespaces? Default to False because it isn't
    # in the SQL standard.
    supports_tablespaces = False

    # Does the backend reset sequences between tests?
    supports_sequence_reset = False

    # Can the backend introspect the default value of a column?
    can_introspect_default = False

    # Confirm support for introspected foreign keys
    # Every database can do this reliably, except MySQL,
    # which can't do it for MyISAM tables
    can_introspect_foreign_keys = False

    # Can the backend introspect the column order (ASC/DESC) for indexes?
    supports_index_column_ordering = False

    # Does the backend support introspection of materialized views?
    can_introspect_materialized_views = True

    # Support for the DISTINCT ON clause
    can_distinct_on_fields = False

    # Does the backend prevent running SQL queries in broken transactions?
    atomic_transactions = False

    # Can we roll back DDL in a transaction?
    can_rollback_ddl = False

    # Does it support operations requiring references rename in a transaction?
    supports_atomic_references_rename = True

    # Can we issue more than one ALTER COLUMN clause in an ALTER TABLE?
    supports_combined_alters = False

    # Does it support foreign keys?
    supports_foreign_keys = False

    # Can it create foreign key constraints inline when adding columns?
    can_create_inline_fk = False

    # Does it automatically index foreign keys?
    indexes_foreign_keys = False

    # Does it support CHECK constraints?
    supports_column_check_constraints = False
    supports_table_check_constraints = False
    # Does the backend support introspection of CHECK constraints?
    can_introspect_check_constraints = False

    # Does the backend support 'pyformat' style ("... %(name)s ...", {'name': value})
    # parameter passing? Note this can be provided by the backend even if not
    # supported by the Python driver
    supports_paramstyle_pyformat = True

    # Does the backend require literal defaults, rather than parameterized ones?
    requires_literal_defaults = False

    # Does the backend require a connection reset after each material schema change?
    connection_persists_old_columns = False

    # Does 'a' LIKE 'A' match?
    has_case_insensitive_like = True

    # Suffix for backends that don't support "SELECT xxx;" queries.
    bare_select_suffix = ""

    # If NULL is implied on columns without needing to be explicitly specified
    implied_column_null = True

    # Does the backend support "select for update" queries with limit (and offset)?
    supports_select_for_update_with_limit = False

    # Does the backend ignore null expressions in GREATEST and LEAST queries unless
    # every expression is null?
    greatest_least_ignores_nulls = False

    # Can the backend clone databases for parallel test execution?
    # Defaults to False to allow third-party backends to opt-in.
    can_clone_databases = False

    # Does the backend consider table names with different casing to
    # be equal?
    ignores_table_name_case = False

    # Place FOR UPDATE right after FROM clause. Used on MSSQL.
    for_update_after_from = False

    # Combinatorial flags
    supports_select_union = False
    supports_select_intersection = False
    supports_select_difference = False
    supports_slicing_ordering_in_compound = False
    supports_parentheses_in_compound = False

    # Does the database support SQL 2003 FILTER (WHERE ...) in aggregate
    # expressions?
    supports_aggregate_filter_clause = False

    # Does the backend support indexing a TextField?
    supports_index_on_text_field = False

    # Does the backend support window expressions (expression OVER (...))?
    supports_over_clause = False
    supports_frame_range_fixed_distance = False
    only_supports_unbounded_with_preceding_and_following = False

    # Does the backend support CAST with precision?
    supports_cast_with_precision = True

    # How many second decimals does the database return when casting a value to
    # a type with time?
    time_cast_precision = 6

    # SQL to create a procedure for use by the Django test suite. The
    # functionality of the procedure isn't important.
    create_test_procedure_without_params_sql = None
    create_test_procedure_with_int_param_sql = None

    # Does the backend support keyword parameters for cursor.callproc()?
    supports_callproc_kwargs = False

    # What formats does the backend EXPLAIN syntax support?
    supported_explain_formats = set()

    # Does DatabaseOperations.explain_query_prefix() raise ValueError if
    # unknown kwargs are passed to QuerySet.explain()?
    validates_explain_options = True

    # Does the backend support the default parameter in lead() and lag()?
    supports_default_in_lead_lag = True

    # Does the backend support ignoring constraint or uniqueness errors during
    # INSERT?
    supports_ignore_conflicts = True

    # Does this backend require casting the results of CASE expressions used
    # in UPDATE statements to ensure the expression has the correct type?
    requires_casted_case_in_updates = False

    # Does the backend support partial indexes (CREATE INDEX ... WHERE ...)?
    supports_partial_indexes = False
    supports_functions_in_partial_indexes = False
    # Does the backend support covering indexes (CREATE INDEX ... INCLUDE ...)?
    supports_covering_indexes = False
    # Does the backend support indexes on expressions?
    supports_expression_indexes = False
    # Does the backend treat COLLATE as an indexed expression?
    collate_as_index_expression = False

    # Does the database allow more than one constraint or index on the same
    # field(s)?
    allows_multiple_constraints_on_same_fields = False

    # Does the backend support boolean expressions in SELECT and GROUP BY
    # clauses?
    supports_boolean_expr_in_select_clause = True

    # Does the backend support JSONField?
    supports_json_field = True
    # Can the backend introspect a JSONField?
    can_introspect_json_field = True
    # Does the backend support primitives in JSONField?
    supports_primitives_in_json_field = True
    # Is there a true datatype for JSON?
    has_native_json_field = False
    # Does the backend use PostgreSQL-style JSON operators like '->'?
    has_json_operators = False
    # Does the backend support __contains and __contained_by lookups for
    # a JSONField?
    supports_json_field_contains = True
    # Does value__d__contains={'f': 'g'} (without a list around the dict) match
    # {'d': [{'f': 'g'}]}?
    json_key_contains_list_matching_requires_list = False
    # Does the backend support JSONObject() database function?
    has_json_object_function = True

    # Does the backend support column collations?
    supports_collation_on_charfield = True
    supports_collation_on_textfield = True
    # Does the backend support non-deterministic collations?
    supports_non_deterministic_collations = True

    # Collation names for use by the Django test suite.
    test_collations = {
        "ci": None,  # Case-insensitive.
        "cs": None,  # Case-sensitive.
        "non_default": None,  # Non-default.
        "swedish_ci": None,  # Swedish case-insensitive.
    }

    # A set of dotted paths to tests in Django's test suite that are expected
    # to fail on this database.
    django_test_expected_failures = set()
    # A map of reasons to sets of dotted paths to tests in Django's test suite
    # that should be skipped for this database.
    django_test_skips = {}
