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

    @property
    def keyspace(self):
        return self.session.keyspace

    def set_keyspace(self, name: str):
        return self.session.set_keyspace(name)

    def _process_rows(self, rows):
        return (tuple(r) for r in rows)

    def execute(self, query: str, parameters=None):
        if not query:
            return None
        logger.debug(f"QUERY {query}, params {parameters}")
        self.result = self.session.execute(query, parameters=parameters)
        rows = self._process_rows(self.result.all())
        return rows

    def fetchmany(self, size=1):
        return self.result.current_rows[:size]

    def fetchone(self):
        return self.result.one()

    def fetchall(self):
        return self.result.all()

    @property
    def lastrowid(self):
        ...
