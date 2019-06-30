"""Defines the exceptions used by SimQLe."""


class NoConnectionsFileError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class UnknownConnectionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class EnvironSyncError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class NoDefaultConnectionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class MultipleDefaultConnectionsError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg
