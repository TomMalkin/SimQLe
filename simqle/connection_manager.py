"""Define ConnectionManager."""

from .logging import logger
from .connection import Connection
from .exceptions import (
    UnknownConnectionError,
    NoDefaultConnectionError,
)


class ConnectionManager:
    """Manage a set of connections from a given config dict."""

    def __init__(self, config, default_connection_name=None):
        """
        Initialise a ConnectionManager.

        Connections are loaded lazily as required, only the config is loaded on initialisation.
        """
        self.config = config
        self.connections = {}
        self.default_connection_name = default_connection_name  # self.load_default_connection()
        logger.info(
            f"ConnectionManager initialised [default_name = {self.default_connection_name}]"
        )

    def get_engine(self, con_name=None):
        """Return the SQLAlchemy Engine of a Connection by it's name."""
        return self.get_connection(con_name).engine

    def get_connection(self, con_name):
        """
        Return a connection object from its name.

        Connection objects are created and saved the first time they are
        called.
        """
        con_name = self.get_con_name(con_name)

        # Return already initialised connection if it exists.
        if con_name in self.connections:
            return self.connections[con_name]

        # A new Connection instance is required.
        for con_config in self.config:
            if con_config["name"] == con_name:
                self.connections[con_name] = Connection(con_config)
                return self.connections[con_name]

        raise UnknownConnectionError(f"Unknown connection {con_name}")

    def get_con_name(self, con_name):
        """Return the connection name taking into account defaults."""
        if con_name:
            return con_name

        if not self.default_connection_name:
            raise NoDefaultConnectionError(
                "No Connection name was specified but no default connection exists."
            )
        return self.default_connection_name
