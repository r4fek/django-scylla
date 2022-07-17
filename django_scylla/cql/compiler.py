from time import time

from django.db.models import AutoField
from django.db.models.sql import compiler


def unique_rowid():
    # TODO: guarantee that this is globally unique
    return int(time() * 1e6)


class SQLCompiler(compiler.SQLCompiler):
    def as_sql(self, *args, **kwargs):
        result, params = super().as_sql(*args, **kwargs)
        # Append ALLOW FILTERING to all select queries
        # TODO: append this only when needed (not PK is used for query)
        if params:
            result += " ALLOW FILTERING"
        return result, params

    def get_order_by(self):
        res = super().get_order_by()
        print("get_order_by", res)
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
