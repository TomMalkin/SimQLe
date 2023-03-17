"""Define the public facing user interface class."""

import os

from yaml import safe_load

from .actioner import DatabaseActioner
from .config_validator import validate_configuration
from .connection_manager import ConnectionManager
from .constants import MODE_MAP
from .container import Record, RecordScalar, RecordSet
from .logging import logger


class Simqle:
    """
    Expose an interface to database connections.

    Run a SQL query against a connection with execute_sql, or do so and return data with recordset,
    record and record_scalar.
    """
    actioner = DatabaseActioner()

    def __init__(self, file_name=None, mode_override=None, _override_config=None):
        """
        Load a Simqle class from a .connection.yaml file.

        The connections chosen are based on the mode that SimQLe is running: production, development
        or testing. This mode is set via the SIMQLE_MODE environment variable, or you can override
        it with the mode_override parameter.

        If _override_config is given, then ignore the file_name parameter.
        """
        self.file_name = file_name
        self.mode = mode_override or os.getenv("SIMQLE_MODE", "production")
        self.section = MODE_MAP.get(self.mode)

        if not self.section:
            raise ValueError(f"Unknown SimQLe Mode: {self.mode}")

        logger.info(f"Simqle mode set [mode={self.mode}]")

        self.full_config = _override_config or self.load_config_from_file(self.file_name)

        validate_configuration(configuration=self.full_config)

        self.config = self.full_config.get(self.section)

        self.default_connection_name = self.full_config.get("default")
        if self.default_connection_name:
            logger.info(f"SimQLe default connection set to {self.default_connection_name}")

        self.connection_manager = ConnectionManager(
            config=self.config,
            default_connection_name=self.default_connection_name,
        )

        # self.actioner = DatabaseActioner()

    @classmethod
    def from_dict(cls, config_dict, mode_override=None):
        """Load a Simqle object from a dict rather than a file name."""
        return cls(mode_override=mode_override, _override_config=config_dict)

    @staticmethod
    def load_config_from_file(file_name):
        """Return the configuration from a given file_name."""
        file_name = file_name or "./.connections.yaml"

        try:
            with open(file_name, mode="r", encoding="utf8") as file:
                config = safe_load(file.read())
                logger.info(f"Configuration loaded from file [file={file_name}]")

                return config

        except FileNotFoundError as exception:
            raise FileNotFoundError(
                f"Cannot find the specified connections file [{file_name}]"
            ) from exception

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
