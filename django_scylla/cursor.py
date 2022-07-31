import logging

from cassandra.cluster import ResultSet, Session, tuple_factory

logger = logging.getLogger(__name__)


class Cursor:
    def __init__(self, session: Session):
        logger.debug("CURSOR: Initialize Cursor")
        self.session = session
        self.session.row_factory = tuple_factory
        self.result: ResultSet = None

    def __del__(self):
        logger.debug("CURSOR: shutdown session")
        self.session.shutdown()

    def close(self):
        ...

    def __iter__(self):
        print("iter result")
        return iter(self.result)

    @property
    def keyspace(self):
        return self.session.keyspace

    @property
    def rowcount(self):
        print("rowcount", res := len(self.result.all()))
        if self.result is None:
            raise RuntimeError

        # TODO: possibly not optimal
        return res

    def set_keyspace(self, name: str):
        return self.session.set_keyspace(name)

    def execute(self, query: str, parameters=None):
        if not query:
            return None
        logger.debug(f"QUERY {query}, params {parameters}")
        self.result = self.session.execute(query, parameters=parameters)
        return self.result

    def fetchmany(self, size=1):
        if size == 1:
            print("fetchmany fetchone")
            return self.fetchone()
        res = self.result.all()[:size]
        print("fetchmany", res)
        return res

    def fetchone(self):
        return self.result.one()

    def fetchall(self):
        print("fetchall")
        return self.result.all()

    @property
    def lastrowid(self):
        print("lastrowid")
        ...
