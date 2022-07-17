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

    def trim_start(self, names_with_path):
        self._lookup_joins = []
        return super().trim_start(names_with_path)

    def join(self, join, reuse=None):
        if isinstance(join, BaseTable):
            return super().join(join, reuse)
        return [self.base_table]

    def add_ordering(self, *ordering):
        if len(ordering) > 1:
            ordering = ordering[0]
        return super().add_ordering(*ordering)

sql.Query = Query
