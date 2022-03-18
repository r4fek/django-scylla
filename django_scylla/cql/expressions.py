from django.db.models import expressions


class Col(expressions.Col):
    def as_scylladb(self, compiler, connection):
        """Do not return alias, just column name"""
        return compiler.quote_name_unless_alias(self.target.column), []


# safe monkey patching: we just add as_scylladb methods here
# so it won't affect other database backends
expressions.Col = Col
