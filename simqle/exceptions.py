"""Defines the exceptions used by SimQLe."""


class DefaultSimqleError(Exception):
    """Raise when no .connections.yaml files are found."""

    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


class NoDefaultConnectionError(DefaultSimqleError):
    """Raise when no con_name was given and no default connection name exists."""


class UnknownSourceTypeError(DefaultSimqleError):
    """Raise when the type of the src given to a SimQLe class is unknown."""


class NoConnectionsFileError(DefaultSimqleError):
    """Raise when no .connections.yaml files are found."""


class MissingFieldError(DefaultSimqleError):
    """Raise when there is a missing field in a connection."""


class UnknownConnectionError(DefaultSimqleError):
    """Raise when the given connection name doesn't have a Connection."""


class EnvironSyncError(DefaultSimqleError):
    """Raise when the environment in dev or test doesn't match production."""


class AmbigiousLoadTypeError(DefaultSimqleError):
    """Raise when both file_name and config is supplised."""


class UnknownSimqleMode(DefaultSimqleError):
    """Raise when the SIMQLE_MODE var isn't a known mode."""


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
