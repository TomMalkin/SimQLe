"""Define DatabaseActioner."""
import time

from .utility import bind_sql
from .connection import Connection
from .container import RecordSet, Record, RecordScalar
from .logging import logger


class DatabaseActioner:
    """Action commands and queries against database connections."""

    def __init__(self):
        pass

    def execute_sql(self, connection: Connection, sql: str, params=None, reference=None):
        """Execute sql against a database connection, and rollback on error."""
        reference = self.get_reference(reference=reference, sql=sql)

        bound_sql = bind_sql(sql, params) if params else sql

        engine_connection = connection.engine.connect()
        transaction = engine_connection.begin()

        logger.info(
            f"Execution query called [connection='{connection.name}', "
            f"reference='{reference}', params={params}]"
        )

        start_time = time.time()

        try:
            engine_connection.execute(bound_sql)
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            engine_connection.close()

        elapsed_time = time.time() - start_time

        logger.info(
            f"Execution query complete [connection='{connection.name}', "
            f"reference='{reference}', params={params}, execution time={elapsed_time:.4f} seconds]"
        )

    def get_data(self, connection: Connection, sql: str, params=None, reference=None):
        """Get the headings and data from a sql query."""
        reference = self.get_reference(reference=reference, sql=sql)

        bound_sql = bind_sql(sql, params) if params else sql

        engine_connection = connection.engine.connect()
        transaction = engine_connection.begin()

        logger.info(
            f"Query called [connection='{connection.name}', "
            f"reference='{reference}', params={params}]"
        )

        start_time = time.time()

        try:
            result = engine_connection.execute(bound_sql)
            data = result.fetchall()
            headings = list(result.keys())
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            engine_connection.close()

        elapsed_time = time.time() - start_time

        logger.info(
            f"Query complete [connection='{connection.name}', "
            f"reference='{reference}', params={params}, execution time={elapsed_time:.4f} seconds]"
        )

        return headings, data

    def recordset(self, connection, sql, params=None, reference=None):
        """Return a RecordSet object from a connection."""
        headings, data = self.get_data(
            connection=connection, sql=sql, params=params, reference=reference
        )
        return RecordSet(headings=headings, data=data)

    def record(self, connection, sql, params=None, reference=None):
        """Return a Record object from a connection."""
        headings, data = self.get_data(
            connection=connection, sql=sql, params=params, reference=reference
        )
        return Record(headings=headings, data=data)

    def record_scalar(self, connection, sql, params=None, reference=None):
        """Return a RecordScalar object from a connection."""
        headings, data = self.get_data(
            connection=connection, sql=sql, params=params, reference=reference
        )
        return RecordScalar(headings=headings, data=data)

    @staticmethod
    def get_reference(reference, sql):
        """
        Return the reference of a query for logging.

        This is the user given reference or the first 20 characters of the query.
        """
        return reference or " ".join(sql.splitlines())[:20]
