import logging

from cassandra.cluster import ResultSet, Session

logger = logging.getLogger(__name__)


class Cursor:
    def __init__(self, session: Session):
        logger.debug("CURSOR: Initialize Cursor")
        self.session = session
        self.result: ResultSet = None

    def __del__(self):
        logger.debug("CURSOR: shutdown session")
        self.session.shutdown()

    def close(self):
        ...

    def __iter__(self):
        return iter(self.result)

    @property
    def keyspace(self):
        return self.session.keyspace

    @property
    def rowcount(self):
        if self.result is None:
            raise RuntimeError

        # TODO: possibly not optimal
        return len(self.result.all())

    def set_keyspace(self, name: str):
        return self.session.set_keyspace(name)

    def execute(self, query: str, parameters=None):
        if not query:
            return None
        logger.debug("QUERY %s, params %s", query, parameters)
        self.result = self.session.execute(query, parameters=parameters)
        return self.result

    def fetchmany(self, size=1):
        if size == 1:
            return self.fetchone()
        res = self.result.all()[:size]
        return res

    def fetchone(self):
        res = self.result.one()
        is_empty = len(res) == 1 and res[0] == 0
        return None if is_empty else res

    def fetchall(self):
        return self.result.all()

    @property
    def lastrowid(self):
        ...
