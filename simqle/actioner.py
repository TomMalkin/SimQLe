"""Define DatabaseActioner."""

from .connection import Connection
from .container import Record, RecordScalar, RecordSet
from .logging import logger
from .timer import Timer
from .utility import bind_sql


class DatabaseActioner:
    """Action commands and queries against database connections."""

    def __init__(self):
        """Initialise the class."""

    def execute_sql(self, connection: Connection, sql: str, params=None, reference=None):
        """Execute sql against a database connection, and rollback on error."""
        reference = self.get_reference(reference=reference, sql=sql)

        bound_sql = bind_sql(sql, params) if params else sql

        transaction = Transaction(connection)

        logger.info(
            f"Execution query called [connection='{connection.name}', "
            f"reference='{reference}', params={params}]"
        )

        timer = Timer()

        try:
            transaction.execute(bound_sql)
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            logger.error(
                f"Execution query error [connection='{connection.name}', "
                f"reference='{reference}', params={params}]"
            )
            raise exception

        finally:
            transaction.finalise()

        elapsed_time = timer.get_elapsed_time()

        logger.info(
            f"Execution query complete [connection='{connection.name}', "
            f"reference='{reference}', params={params}, execution time={elapsed_time:.4f} seconds]"
        )

    def get_data(self, connection: Connection, sql: str, params=None, reference=None):
        """Get the headings and data from a sql query."""
        reference = self.get_reference(reference=reference, sql=sql)

        bound_sql = bind_sql(sql, params) if params else sql

        transaction = Transaction(connection)

        logger.info(
            f"Query called [connection='{connection.name}', "
            f"reference='{reference}', params={params}]"
        )

        timer = Timer()

        try:
            headings, data = transaction.get_data(bound_sql)
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            logger.error(
                f"Get data query error [connection='{connection.name}', "
                f"reference='{reference}', params={params}]"
            )
            raise exception

        finally:
            transaction.finalise()

        elapsed_time = timer.get_elapsed_time()

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
        return reference or " ".join([line.strip() for line in sql.splitlines()]).strip()[:20]


class Transaction:
    """Manage a transaction using an engine."""

    def __init__(self, connection: Connection):
        """Initialise a Transaction using a connection."""
        # self.connection = connection
        # self.engine = self.connection.engine.connect()
        # self.transaction = self.engine.begin()

        self.connection = connection
        self.engine = self.get_engine()
        self.connected_engine = self.connect_engine()
        self.communication = self.begin_transaction()

        # engine = self.get_engine(connection)
        # self.connected_engine = self.connect_engine(engine)
        # self.transaction = self.begin_transaction(self.connected_engine)

    def get_engine(self):
        """Get the SQL Alchemy engine from a Connection."""
        return self.connection.engine

    def connect_engine(self):
        """Connect the engine to the database."""
        return self.engine.connect()

    def begin_transaction(self):
        """Start a transaction."""
        return self.connected_engine.begin()

    def rollback(self):
        """Use the rollback function of a transaction."""
        self.communication.rollback()

    def finalise(self):
        """If the query was successful, then finalise the transaction."""
        self.connected_engine.close()

    def execute(self, bound_sql):
        """Execute sql against the transaction."""
        self.connected_engine.execute(bound_sql)

    def commit(self):
        """Commit the current transaction to the database."""
        self.communication.commit()

    def get_data(self, bound_sql):
        """Get data from a transaction."""
        result = self.connected_engine.execute(bound_sql)
        data = result.fetchall()
        headings = list(result.keys())
        return headings, data
