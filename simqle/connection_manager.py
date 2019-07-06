"""Defines the ConnectionManager and Connection Classes."""

import os
from yaml import safe_load
from sqlalchemy import create_engine
from sqlalchemy.sql import text, bindparam
from sqlalchemy.types import VARCHAR
from urllib.parse import quote_plus
from simqle.constants import DEFAULT_FILE_LOCATIONS, DEV_MAP
from simqle.exceptions import (
    NoConnectionsFileError, UnknownConnectionError,
    MultipleDefaultConnectionsError, EnvironSyncError, UnknownSimqleMode,
    NoDefaultConnectionError,
)


class ConnectionManager:
    """
    The Connection Manager Class.

    Create an instance of this class with a yaml configuration file. If no
    yaml file is given, the first connection file found in default locations
    will be used instead.

    This is the class from which you execute sql and return recordsets, using
    the public methods self.execute_sql and self.recordset.
    """

    def __init__(self, file_name=None):
        """
        Initialise a ConnectionManager.

        Connections are loaded lazily as required, only the config is loaded
        on initialisation.
        """
        self.connections = {}

        # For backwards compatibility, test mode is given precedence
        if isinstance(os.getenv("SIMQLE_TEST"), str) and os.getenv(
                "SIMQLE_TEST").lower() == "true":
            self.dev_mode = "testing"
            self.dev_type = "test-connections"

        else:
            self.dev_mode = os.getenv("SIMQLE_MODE", "production")
            self.dev_type = DEV_MAP.get(self.dev_mode)

            if not self.dev_type:
                error_msg = "{} is an unknown simqle mode".format(
                    self.dev_mode)
                raise UnknownSimqleMode(error_msg)

        # self.test_mode = os.getenv("SIMQLE_TEST", False)
        # self.dev_type = DEV_MAP[bool(self.test_mode)]

        self._default_connection_name = None

        if not file_name:
            # file_name isn't given so we search through the possible default
            # file locations, which are in order of priority.
            for default_file_name in DEFAULT_FILE_LOCATIONS:
                try:
                    self.config = self._load_yaml_file(default_file_name)
                    return
                except:  # noqa TODO: add file not found specific exception.
                    continue

            raise NoConnectionsFileError(
                "No file_name is specified and no files in default "
                "locations are found.")

        else:
            self.config = self._load_yaml_file(file_name)

        self._check_default_connections()

    # --- Public Methods: ---

    def recordset(self, sql, con_name=None, params=None):
        """Return recordset from connection."""
        con_name = self._con_name(con_name)
        connection = self._get_connection(con_name)
        return connection.recordset(sql, params=params)

    def execute_sql(self, sql, con_name=None, params=None):
        """Execute SQL on a given connection."""
        con_name = self._con_name(con_name)
        connection = self._get_connection(con_name)
        connection.execute_sql(sql, params=params)

    def get_engine(self, con_name=None):
        """Return the engine of a Connection by it's name."""
        con_name = self._con_name(con_name)
        return self._get_connection(con_name).engine

    def get_connection(self, con_name=None):
        """
        Return the engine of a Connection by it's name.

        Deprecated, only exists for backwards compatibility.
        """
        con_name = self._con_name(con_name)
        return self.get_engine(con_name)  # TODO: add warning

    def reset_connections(self):
        """Remove all current connection objects."""
        self.connections = {}
        self._default_connection_name = None

    # --- Private Methods: ---

    def _load_yaml_file(self, connections_file):
        """Load the configuration from the given file."""
        with open(connections_file) as file:
            return safe_load(file.read())

    def _get_connection(self, conn_name):
        """
        Return a connection object from its name.

        Connection objects are created and saved the first time they are
        called.
        """
        # TODO: make conn_name and con_name consistent across the project

        # Return already initialised connection if it exists.
        if conn_name in self.connections:
            return self.connections[conn_name]

        # A new Connection instance is required.
        for conn_config in self.config[self.dev_type]:
            if conn_config["name"] == conn_name:
                self.connections[conn_name] = _Connection(conn_config)
                return self.connections[conn_name]

        raise UnknownConnectionError("Unknown connection {}".format(conn_name))

    def _check_default_connections(self):
        """Check that default settings are set correctly."""
        # See if a default connection exists
        number_of_defaults = 0
        for connection in self.config["connections"]:
            if connection.get("default"):
                number_of_defaults += 1
                self._default_connection_name = connection.get("name")

        if not number_of_defaults:
            return

        if number_of_defaults > 1:
            raise MultipleDefaultConnectionsError(
                "More than 1 default connection was specified.")

        if not self.config.get("test-connections"):
            return

        for connection in self.config["test-connections"]:
            if connection.get("default"):
                if connection.get("name") != self._default_connection_name:
                    raise EnvironSyncError("The default connection in "
                                           "connections doesn't match the "
                                           "default connection in the test "
                                           "connections.")

    def _con_name(self, con_name=None):
        if con_name:
            return con_name

        return self._get_default_connection()

    def _get_default_connection(self):
        if not self._default_connection_name:
            raise NoDefaultConnectionError("No Connection name was specified "
                                           "but no default connection exists.")
        return self._default_connection_name


class _Connection:
    """
    The _Connection class.

    This represents a single connection. This class also managers the execution
    of SQL, including the management of transactions.

    The engine is lazily loaded the first time either execute_sql or recordset
    is called.

    This class shouldn't be loaded outside the ConnectionManager class, and so
    is marked as internal only.
    """

    def __init__(self, conn_config):
        """Create a new Connection from a config dict."""
        self.driver = conn_config['driver']
        self._engine = None

        # Edit the connection based on configuration options.

        # for Microsoft ODBC connections, for example, the connection string
        # must be url escaped. We do this for the user if the url_escape
        # option is True. See here for example and more info:
        # https://docs.sqlalchemy.org/en/13/dialects/mssql.html
        #   #pass-through-exact-pyodbc-string
        if 'url_escape' in conn_config:
            self.connection_string = quote_plus(conn_config['connection'])
        else:
            self.connection_string = conn_config['connection']

    def _connect(self):
        """Create an engine based on sqlalchemy's create_engine."""
        self._engine = create_engine(self.driver + self.connection_string)

    @property
    def engine(self):
        """Load the engine if it hasn't been loaded before."""
        if not self._engine:
            self._connect()

        return self._engine

    def execute_sql(self, sql, params=None):
        """Execute :sql: on this connection with named :params:."""
        bound_sql = _Connection._bind_sql(sql, params)

        # TODO: discuss whether a connection should be closed on each
        # transaction.
        connection = self.engine.connect()
        transaction = connection.begin()

        # execute the query, and rollback on error
        try:
            connection.execute(bound_sql)
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            connection.close()

    def recordset(self, sql, params=None):
        """
        Execute <sql> on <con>, with named <params>.

        Return (data, headings)
        """
        # bind the named parameters.
        bound_sql = self._bind_sql(sql, params)

        # start the connection.
        connection = self.engine.connect()
        transaction = connection.begin()

        # get the results from the query.
        result = connection.execute(bound_sql)
        data = result.fetchall()
        headings = result.keys()

        # commit and close the connection
        transaction.commit()
        connection.close()

        return data, headings

    @staticmethod
    def _bind_sql(sql, params):
        bound_sql = text(sql)  # convert to the useful sqlalchemy text

        if params:  # add the named parameters
            bound_sql = _Connection._bind_params(bound_sql, params)

        return bound_sql

    @staticmethod
    def _bind_params(bound_sql, params):
        """Bind named parameters to the given sql."""
        for key, value in params.items():
            if isinstance(value, str):
                bound_sql = bound_sql.bindparams(
                    bindparam(key=key, value=value, type_=VARCHAR(None))
                )
            else:
                bound_sql = bound_sql.bindparams(
                    bindparam(key=key, value=value)
                )
        return bound_sql
