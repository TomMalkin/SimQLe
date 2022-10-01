"""Define the public facing user interface class."""

from .actioner import DatabaseActioner
from .config_loader import ConfigLoader, load_default_connection_name
from .connection_manager import ConnectionManager
from .container import Record, RecordScalar, RecordSet
from .logging import logger
from .mode_loader import mode_loader


class Simqle:
    """
    Expose an interface to database connections.

    Run a SQL query against a connection with execute_sql, or do so and return data with recordset,
    record and record_scalar.
    """

    def __init__(self, src=None, mode_override=None):
        """
        Load a Simqle class from a src.

        The options for the source are a str, which will be a file path to a .connections.yaml file.
        Or a dict, in which case that is loaded as the config. Or it is None, in which case default
        locations are searched, starting with the directory that python was called from.

        The connections chosen are based on the mode that SimQLe is running: production, development
        or testing.

        The general set up of this class is:

        The src is loaded using a ConfigLoader outputting a config dict. The config is then passed
        to a ConnectionManager that handles all the named connections we might want. We get a
        connection from the ConnectionManager, and execute SQL against it using a DatabaseActioner.
        """
        self.src = src
        self.mode = mode_loader(override=mode_override)
        logger.info(f"Simqle mode set [mode={self.mode}]")

        self.config = self._load_config(self.src, self.mode)

        self.default_connection_name = load_default_connection_name(self.config)
        logger.info(f"SimQLe default connection set to {self.default_connection_name}")

        self.connection_manager = self._load_connection_manager()

        self.actioner = DatabaseActioner()

    def _load_connection_manager(self):
        return ConnectionManager(
            config=self.config,
            default_connection_name=self.default_connection_name,
        )

    @staticmethod
    def _load_config(src, mode):
        """Load the config from a given src and mode."""
        return ConfigLoader(src, mode=mode).config

    def execute_sql(self, sql, con_name=None, params=None, reference=None):
        """Execute SQL against a named connection and details."""
        connection = self.connection_manager.get_connection(con_name=con_name)
        self.actioner.execute_sql(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )

    def recordset(self, sql, con_name=None, params=None, reference=None) -> RecordSet:
        """Get a RecordSet from a named connection and query details."""
        connection = self.connection_manager.get_connection(con_name=con_name)
        recordset = self.actioner.recordset(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )
        return recordset

    def record(self, sql, con_name=None, params=None, reference=None) -> Record:
        """Get a Record from a named connection and query details."""
        connection = self.connection_manager.get_connection(con_name=con_name)
        record = self.actioner.record(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )
        return record

    def record_scalar(self, sql, con_name=None, params=None, reference=None) -> RecordScalar:
        """Get a RecordScalar from a named connection and query details."""
        connection = self.connection_manager.get_connection(con_name=con_name)
        record_scalar = self.actioner.record_scalar(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )
        return record_scalar
