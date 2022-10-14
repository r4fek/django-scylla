import logging

from django.db.models import sql
from django.db.models.sql.datastructures import BaseTable

from django_scylla.cql.where import WhereNode

logger = logging.getLogger(__name__)


class Query(sql.query.Query):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.where = WhereNode()

    def setup_joins(self, names, opts, alias, can_reuse=None, allow_many=True):
        join_info = super().setup_joins(
            names, opts, alias, can_reuse=can_reuse, allow_many=allow_many
        )

        def final_transformer(field, alias):
            if not self.alias_cols:
                alias = None
            return field.get_col(alias)

        join_info = sql.query.JoinInfo(
            join_info.final_field,
            join_info.targets,
            join_info.opts,
            [join_info.joins[0]],
            [],
            final_transformer,
        )
        return join_info

    def clear_where(self):
        self.where = WhereNode()

    def trim_start(self, names_with_path):
        self._lookup_joins = []
        return super().trim_start(names_with_path)

    def join(self, join, reuse=None):
        if isinstance(join, BaseTable):
            return super().join(join, reuse)
        return [self.base_table]

    def add_ordering(self, *ordering):
        if len(ordering) > 1:
            ordering = [ordering[0]]
        return super().add_ordering(*ordering)

    def add_select_related(self, fields):
        ...

    def exists(self, using, limit=True):
        q = self.clone()
        if not q.distinct:
            if q.group_by is True:
                q.add_fields(
                    (f.attname for f in self.model._meta.concrete_fields), False
                )
                # Disable GROUP BY aliases to avoid orphaning references to the
                # SELECT clause which is about to be cleared.
                q.set_group_by(allow_aliases=False)
            q.clear_select_clause()
        q.clear_ordering(force=True)
        if limit:
            q.set_limits(high=1)
        q.add_extra({"a": "count(*)"}, None, None, None, None, None)
        q.set_extra_mask(None)
        return q


sql.Query = Query
