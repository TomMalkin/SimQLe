"""Define ConnectionManager."""

from .connection import Connection
from .exceptions import NoDefaultConnectionError, UnknownConnectionError
from .logging import logger


class ConnectionManager:
    """Manage a set of connections from a given config dict."""

    def __init__(self, config, default_connection_name):
        """
        Initialise a ConnectionManager.

        Connections are loaded lazily as required, only the config is loaded on initialisation.
        """
        self.config = config
        self.connections = {}
        self._default_connection_name = default_connection_name
        logger.info(
            f"ConnectionManager initialised [default_name = {self._default_connection_name}]"
        )

    @property
    def default_connection_name(self):
        """Get the default connection name with the assumption that it exists."""
        if not self._default_connection_name:
            raise NoDefaultConnectionError(
                "No Connection name was specified but no default connection exists."
            )

        return self._default_connection_name

    def get_engine(self, con_name=None):
        """Return the SQLAlchemy Engine of a Connection by it's name."""
        return self.get_connection(con_name).engine

    def get_connection(self, con_name):
        """
        Return a connection object from its name.

        Connection objects are created and saved the first time they are
        called.
        """
        if not con_name:
            con_name = self.default_connection_name

        # Return already initialised connection if it exists.
        if con_name in self.connections:
            return self.connections[con_name]

        # A new Connection instance is required.
        for con_config in self.config:
            if con_config["name"] == con_name:
                self.connections[con_name] = Connection(con_config)
                return self.connections[con_name]

        raise UnknownConnectionError(f"Unknown connection {con_name}")
