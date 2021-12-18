from time import time

from django.db.models import AutoField
from django.db.models.sql import compiler


def unique_rowid():
    # TODO: guarantee that this is globally unique
    return int(time() * 1e6)

class SQLCompiler(compiler.SQLCompiler):
    ...


class SQLInsertCompiler(compiler.SQLInsertCompiler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pk_fields = [f for f in self.query.model._meta.get_fields() if f.primary_key]
        self.query.fields = pk_fields + self.query.fields

    def prepare_value(self, field, value):
        if value is None and isinstance(field, AutoField):
            value = unique_rowid()
        return super().prepare_value(field, value)
