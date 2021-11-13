"""Define the public facing user interface class."""

from .connection_manager import ConnectionManager
from .config_loader import ConfigLoader
from .mode_loader import mode_loader
from .actioner import DatabaseActioner
from .container import RecordSet, Record, RecordScalar
from .logging import logger


class Simqle:
    """Expose an interface to database connections."""

    def __init__(self, file_name=None, mode_override=None):

        self.mode = mode_loader(override=mode_override)

        logger.info(f"Simqle mode set [mode={self.mode}]")

        self.config_loader = ConfigLoader(file_name, mode=self.mode)
        self.config = self.config_loader.config
        self.default_connection_name = self.config_loader.default_connection_name

        self.connection_manager = ConnectionManager(
            config=self.config,
            default_connection_name=self.default_connection_name,
        )
        self.actioner = DatabaseActioner()

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
