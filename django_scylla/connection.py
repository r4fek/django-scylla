

class ConnectionWrapper:
    def __init__(self, session):
        self.session = session

    def close(self):
        ...

    def set_keyspace(self, name):
        return self.session.set_keyspace(name)
