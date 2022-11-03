from django.db.models.constraints import BaseConstraint


class PrimaryKeysConstraint(BaseConstraint):
    def __init__(self, fields=()):
        if not fields:
            raise ValueError("fields argument is missing")

        self.fields = tuple(fields)
        super().__init__(self.__class__.__name__)

    def constraint_sql(self, model, schema_editor):
        return schema_editor._create_primary_keys_sql(self.fields)

    def create_sql(self, model, schema_editor):
        return ""

    def remove_sql(self, model, schema_editor):
        return ""
