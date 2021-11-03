"""Define ConnectionManager."""

import os
import time
import uuid

from yaml import safe_load
from sqlalchemy import create_engine

from urllib.parse import quote_plus

from .constants import DEFAULT_FILE_LOCATIONS, DEV_MAP
from .utility import bind_sql
from .actioner import DatabaseActioner
from .container import RecordSet, RecordScalar, Record
from .logging import logger as log
from .connection import Connection
from .exceptions import (
    NoConnectionsFileError,
    UnknownConnectionError,
    MultipleDefaultConnectionsError,
    EnvironSyncError,
    UnknownSimqleMode,
    NoDefaultConnectionError,
)


class ConnectionManager:
    """
    This class manages a set of connections from a given config dict.
    """
    """
    The Connection Manager Class.

    Create an instance of this class with a yaml configuration file. If no yaml file is given, the
    first connection file found in default locations will be used instead.

    This is the class from which you execute sql and return recordsets, using the public methods
    self.execute_sql and self.recordset.
    """

    def __init__(self, config):
        """
        Initialise a ConnectionManager.

        Connections are loaded lazily as required, only the config is loaded on initialisation.
        """

        self.config = config
        self.connections = {}
        self.default_connection_name = None

        # self.mode = self._get_mode()
        # self.mode_name = self._get_mode_name(self.mode)

        # log.info(f"ConnectionManager is set to [{self.mode}] mode")

        # self.config = self._load_config(file_name)

        self.default_connection_name = self.load_default_connection()

    # --- Public Methods: ---

    def recordset(self, sql, con_name=None, params=None, reference=None):
        headings, data = self._recordset(sql, con_name, params=params, reference=reference)
        return RecordSet(headings=headings, data=data)

    def record(self, sql, con_name=None, params=None, reference=None):
        headings, data = self._recordset(sql, con_name, params=params, reference=reference)
        return Record(headings=headings, data=data)

    def record_scalar(self, sql, con_name=None, params=None, reference=None):
        headings, data = self._recordset(sql, con_name, params=params, reference=reference)
        return RecordScalar(headings=headings, data=data)

    def execute_sql(self, sql, con_name=None, params=None, reference=None):
        """Execute SQL on a given connection."""
        query_id = uuid.uuid4()
        reference = self._get_reference(reference)
        con_name = self._con_name(con_name)

        log.debug(
            f"Execution query starting [{con_name=}, {query_id=}, {params=}, {reference=}, {sql=}]"
        )

        connection = self._get_connection(con_name)

        start_time = time.time()

        connection.execute_sql(sql, params=params)

        elapsed_time = time.time() - start_time

        log.info(
            f"Execution query completed [Query Id={query_id}, Reference={reference}, Connection Name={con_name}, "
            f"Params={params}, Execution Time={elapsed_time:.4f} seconds]"
        )

    def get_engine(self, con_name=None):
        """Return the engine of a Connection by it's name."""
        con_name = self._con_name(con_name)
        return self._get_connection(con_name).engine

    # --- Private Methods: ---

    def _recordset(self, sql, con_name=None, params=None, reference=None):
        """Return headings and data from a connection."""
        query_id = uuid.uuid4()
        reference = self._get_reference(reference)

        log.debug(
            f"Recordset query starting [{con_name=}, {query_id=}, {params=}, {reference=}, {sql=}]"
        )

        start_time = time.time()
        con_name = self._con_name(con_name)
        connection = self._get_connection(con_name)
        rst = connection.recordset(sql, params=params, reference=None)
        elapsed_time = time.time() - start_time

        log.info(
            f"Recordset query completed [Query Id={query_id}, Reference={reference}, Connection Name={con_name}, "
            f"Params={params}, Execution Time={elapsed_time:.4f} seconds]"
        )

        return rst

    @staticmethod
    def _get_reference(reference, sql):
        """
        Return the reference of a query for logging.

        This is the user given reference or the first 20 characters of the query.
        """
        reference = reference or " ".join(sql.splitlines())[:20]

    @staticmethod
    def _load_yaml_file(connections_file):
        """Load the configuration from the given file."""
        with open(connections_file) as file:
            return safe_load(file.read())

    def _get_connection(self, con_name):
        """
        Return a connection object from its name.

        Connection objects are created and saved the first time they are
        called.
        """
        # Return already initialised connection if it exists.
        if con_name in self.connections:
            return self.connections[con_name]

        # A new Connection instance is required.
        for conn_config in self.config[self.mode_name]:
            if conn_config["name"] == con_name:
                self.connections[con_name] = _Connection(conn_config)
                return self.connections[con_name]

        raise UnknownConnectionError("Unknown connection {}".format(con_name))

    def load_default_connection(self):
        """Check that default settings are set correctly."""
        # See if a default connection exists
        number_of_defaults = 0
        for connection in self.config["connections"]:
            if connection.get("default"):
                number_of_defaults += 1
                _default_connection_name = connection.get("name")

                log.info(f"Setting the default connection to " f"{connection.get('name')}")

        if not number_of_defaults:
            return

        if number_of_defaults > 1:
            raise MultipleDefaultConnectionsError("More than 1 default connection was specified.")

        if "dev-connections" in self.config:
            _default_connection_name_dev = ""
            number_of_defaults_dev = 0

            for connection in self.config["dev-connections"]:
                if connection.get("default"):
                    number_of_defaults_dev += 1
                    _default_connection_name_dev = connection.get("name")

            if number_of_defaults > 1:
                raise MultipleDefaultConnectionsError(
                    "More than 1 default connection was specified in the dev-connections."
                )

            if _default_connection_name != _default_connection_name_dev:
                raise EnvironSyncError(
                    "The default connections in production and development do not match, "
                    f"the production default is [{_default_connection_name}] and the dev default "
                    f"is [{_default_connection_name_dev}]"
                )

        if "test-connections" in self.config:
            _default_connection_name_test = ""
            number_of_defaults_test = 0

            for connection in self.config["test-connections"]:
                if connection.get("default"):
                    number_of_defaults_test += 1
                    _default_connection_name_test = connection.get("name")

            if number_of_defaults > 1:
                raise MultipleDefaultConnectionsError(
                    "More than 1 default connection was specified in the test-connections."
                )

            if _default_connection_name != _default_connection_name_test:
                raise EnvironSyncError(
                    "The default connections in production and testing do not match, "
                    f"the production default is [{_default_connection_name}] and the test default "
                    f"is [{_default_connection_name_test}]"
                )

        return _default_connection_name

    def _con_name(self, con_name=None):
        if con_name:
            return con_name

        return self._get_default_connection()

    def _get_default_connection(self):
        if not self.default_connection_name:
            raise NoDefaultConnectionError(
                "No Connection name was specified " "but no default connection exists."
            )
        return self.default_connection_name

    @staticmethod
    def _get_mode():
        """
        Get the mode that the ConnectionManager should be running in given
        Environment Variable settings.
        """
        # For backwards compatibility, test mode is given precedence
        if isinstance(os.getenv("SIMQLE_TEST"), str) and os.getenv("SIMQLE_TEST").lower() == "true":

            log.warn(
                "ConnectionManager set to test mode because SIMQLE_TEST is set. "
                "SIMQLE_TEST is deprecated, please use SIMQLE_MODE instead."
            )

            return "testing"

        else:
            return os.getenv("SIMQLE_MODE", "production")

    @staticmethod
    def _get_mode_name(mode):
        """Get the name of the title used in the .connections.yaml file."""
        mode_name = DEV_MAP.get(mode)

        if not mode_name:
            raise UnknownSimqleMode(f"{mode} is an unknown simqle mode")

    def _load_config(self, file_name):
        """
        Return the config dict for a given file_name parameter.

        If the file_name parameter isn't specified, then we search through default
        locations and load from the first one found.

        If the file_name passed is a of a dict type, then just load that as the
        config.
        """
        if not file_name:

            config = None

            log.debug("file_name isn't known so checking default file locations.")

            for default_file_name in DEFAULT_FILE_LOCATIONS:
                try:
                    config = self._load_yaml_file(default_file_name)

                    log.info(
                        f"The connections file was loaded from the default "
                        f"location [{default_file_name}]"
                    )

                    return config

                except FileNotFoundError:
                    continue

            if not config:
                raise NoConnectionsFileError(
                    "No file_name is specified and no files in default " "locations are found."
                )

        else:
            if isinstance(file_name, dict):
                config = file_name

                log.info(f"The connections config was loaded from a dict")

                return config

            else:
                try:
                    self.config = self._load_yaml_file(file_name)
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"Cannot find the specified connections file [{file_name}]"
                    )

                log.info(f"The connections file was loaded from " f"{file_name}")


