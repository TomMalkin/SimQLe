"""Defines the exceptions used by SimQLe."""


class NoConnectionsFileError(Exception):
    """Raise when no .connections.yaml files are found."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class UnknownConnectionError(Exception):
    """Raise when the given connection name doesn't have a Connection."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class EnvironSyncError(Exception):
    """Raise when the environment in dev or test doesn't match production."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class NoDefaultConnectionError(Exception):
    """Raise when no con_name is given but there isn't a default connection in the config."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class MultipleDefaultConnectionsError(Exception):
    """Raise when a config has multiple default connections."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class UnknownSimqleMode(Exception):
    """Raise when the SIMQLE_MODE var isn't a known mode."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class UnknownHeadingError(Exception):
    """Raise when a heading is asked for but the query doesn't have that heading."""

    def __init__(self, heading):
        msg = f"Unknown heading: [{heading}]"
        super().__init__(msg)
        self.message = msg


class NoScalarDataError(Exception):
    """Raise when a record_scalar returns no rows."""

    def __init__(self):
        msg = "No datum was returned"
        super().__init__(msg)
        self.message = msg
