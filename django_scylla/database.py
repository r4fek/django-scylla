from logging import getLogger

from cassandra.cluster import Cluster

logger = getLogger(__name__)
clients = {}


def initialize(db, **kwargs):
    try:
        return clients[db]
    except KeyError:
        logger.debug("Initialize ScyllaDB connection")
        clients[db] = Cluster(**kwargs)
    return clients[db]


class Error(Exception):  # NOQA: StandardError undefined on PY3
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class DataError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class InternalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass
