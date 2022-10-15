from time import time

from django.core.exceptions import EmptyResultSet
from django.db import NotSupportedError
from django.db.models import AutoField
from django.db.models.sql import compiler


def unique_rowid():
    # TODO: guarantee that this is globally unique
    return int(time() * 1e6)


class SQLCompiler(compiler.SQLCompiler):
    def get_extra_select(self, order_by, select):
        return []

    def as_sql(self, with_limits=True, with_col_aliases=False):
        """
        Create the SQL for this query. Return the SQL string and list of
        parameters.

        If 'with_limits' is False, any limit/offset information is not included
        in the query.
        """
        refcounts_before = self.query.alias_refcount.copy()
        try:
            extra_select, order_by, group_by = self.pre_sql_setup()
            for_update_part = None
            # Is a LIMIT/OFFSET clause needed?
            with_limit_offset = with_limits and (
                self.query.high_mark is not None or self.query.low_mark
            )
            combinator = self.query.combinator
            features = self.connection.features
            if combinator:
                if not getattr(features, "supports_select_{}".format(combinator)):
                    raise NotSupportedError(
                        "{} is not supported on this database backend.".format(
                            combinator
                        )
                    )
                result, params = self.get_combinator_sql(
                    combinator, self.query.combinator_all
                )
            else:
                distinct_fields, distinct_params = self.get_distinct()
                # This must come after 'select', 'ordering', and 'distinct'
                # (see docstring of get_from_clause() for details).
                from_, f_params = self.get_from_clause()
                try:
                    where, w_params = (
                        self.compile(self.where) if self.where is not None else ("", [])
                    )
                except EmptyResultSet:
                    if self.elide_empty:
                        raise
                    # Use a predicate that's always False.
                    where, w_params = "0 = 1", []
                having, h_params = (
                    self.compile(self.having) if self.having is not None else ("", [])
                )
                result = ["SELECT"]
                params = []

                if self.query.distinct:
                    distinct_result, distinct_params = self.connection.ops.distinct_sql(
                        distinct_fields,
                        distinct_params,
                    )
                    result += distinct_result
                    params += distinct_params

                out_cols = []
                for _, (s_sql, s_params), alias in self.select:
                    params.extend(s_params)
                    if s_sql[0] == "(" and s_sql[-1] == ")":
                        s_sql = s_sql[1:-1]
                    out_cols.append(s_sql)

                result += [", ".join(out_cols), "FROM", *from_]
                params.extend(f_params)

                if where:
                    result.append("WHERE %s" % where)
                    params.extend(w_params)

                grouping = []
                for g_sql, g_params in group_by:
                    grouping.append(g_sql)
                    params.extend(g_params)
                if grouping:
                    if distinct_fields:
                        raise NotImplementedError(
                            "annotate() + distinct(fields) is not implemented."
                        )
                    order_by = order_by or self.connection.ops.force_no_ordering()
                    result.append("GROUP BY %s" % ", ".join(grouping))
                    if self._meta_ordering:
                        order_by = None
                if having:
                    result.append("HAVING %s" % having)
                    params.extend(h_params)

            if self.query.explain_info:
                result.insert(
                    0,
                    self.connection.ops.explain_query_prefix(
                        self.query.explain_info.format,
                        **self.query.explain_info.options,
                    ),
                )

            if order_by:
                ordering = []
                for _, (o_sql, o_params, _) in order_by:
                    ordering.append(o_sql)
                    params.extend(o_params)
                result.append("ORDER BY %s" % ", ".join(ordering))

            if with_limit_offset:
                result.append(
                    self.connection.ops.limit_offset_sql(
                        self.query.low_mark, self.query.high_mark
                    )
                )

            if for_update_part and not features.for_update_after_from:
                result.append(for_update_part)

            if self.query.subquery and extra_select:
                raise NotSupportedError("Subqueries are not supported.")

            result.append("ALLOW FILTERING")
            return " ".join(result), tuple(params)
        finally:
            # Finally do cleanup - get rid of the joins we created above.
            self.query.reset_refcounts(refcounts_before)

    def get_order_by(self):
        # TODO: fix this!
        return []


class SQLInsertCompiler(compiler.SQLInsertCompiler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pk_fields = [
            f
            for f in self.query.model._meta.get_fields()
            if getattr(f, "primary_key", False)
        ]
        self.query.fields = pk_fields + self.query.fields

    def prepare_value(self, field, value):
        if value is None and isinstance(field, AutoField):
            value = unique_rowid()
        return super().prepare_value(field, value)


class SQLUpdateCompiler(compiler.SQLUpdateCompiler):
    def as_sql(self, *args, **kwargs):
        result, params = super().as_sql(*args, **kwargs)
        result += " IF EXISTS"
        return result, params


class SQLDeleteCompiler(compiler.SQLDeleteCompiler):
    ...
