"""Define the public facing user interface class."""

from .connection_manager import ConnectionManager
from .config_loader import ConfigLoader
from .mode_loader import ModeLoader
from .actioner import DatabaseActioner
from .container import Recordset, Record, RecordScalar
from .logging import logger


class Simqle:
    def __init__(self, file_name=None, mode_override=None):

        self.mode = ModeLoader(override=mode_override).mode

        logger.info(f"Simqle mode set [mode={self.mode}]")

        self.config = ConfigLoader(file_name, mode=self.mode).config
        self.connection_manager = ConnectionManager(config=self.config)
        self.actioner = DatabaseActioner()

    def execute_sql(self, sql, con_name=None, params=None, reference=None):
        connection = self.connection_manager.get_connection(con_name=con_name)
        self.actioner.execute_sql(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )

    def recordset(self, sql, con_name=None, params=None, reference=None) -> Recordset:
        connection = self.connection_manager.get_connection(con_name=con_name)
        recordset = self.actioner.recordset(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )
        return recordset

    def record(self, sql, con_name=None, params=None, reference=None) -> Record:
        connection = self.connection_manager.get_connection(con_name=con_name)
        record = self.actioner.record(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )
        return record

    def recordscalar(self, sql, con_name=None, params=None, reference=None) -> RecordScalar:
        connection = self.connection_manager.get_connection(con_name=con_name)
        record_scalar = self.actioner.recordscalar(
            connection=connection,
            sql=sql,
            params=params,
            reference=reference,
        )
        return record_scalar
