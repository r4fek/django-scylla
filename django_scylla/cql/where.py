from django.db.models.sql import where


class WhereNode(where.WhereNode):
    def as_scylladb(self, compiler, connection):
        res, params = super().as_sql(compiler, connection)
        # ScyllaDB does not support parentheses after WHERE
        if res and res[0] == "(" and res[-1] == ")":
            return res[1:-1], params
        return res, params


class ExtraWhere(where.ExtraWhere):
    def as_sql(self, compiler=None, connection=None):
        sqls = ["%s" % sql for sql in self.sqls]
        return " AND ".join(sqls), list(self.params or ())


where.WhereNode = WhereNode
