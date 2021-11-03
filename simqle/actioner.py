"""Define DatabaseActioner."""

from .utility import bind_sql
from .connection import Connection
from .container import RecordSet, Record, RecordScalar


class DatabaseActioner:
    def __init__(self):
        pass

    def execute_sql(self, connection: Connection, sql: str, params=None):
        """Execute sql against a database connection, and rollback on error."""
        bound_sql = bind_sql(sql, params) if params else sql

        engine_connection = connection.engine.connect()
        transaction = engine_connection.begin()

        try:
            engine_connection.execute(bound_sql)
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            engine_connection.close()

    def get_data(self, connection: Connection, sql: str, params=None):
        """Get the headings and data from a sql query."""
        bound_sql = bind_sql(sql, params) if params else sql

        connection = self.engine.connect()
        transaction = connection.begin()

        try:
            result = connection.execute(bound_sql)
            data = result.fetchall()
            headings = list(result.keys())
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            connection.close()

        return headings, data

    def recordset(self, connection, sql, params=None):
        headings, data = self.get_data(connection=connection, sql=sql, params=params)
        return RecordSet(headings=headings, data=data)

    def record(self, connection, sql, params=None):
        headings, data = self.get_data(connection=connection, sql=sql, params=params)
        return Record(headings=headings, data=data)

    def recordscalar(self, connection, sql, params=None):
        headings, data = self.get_data(connection=connection, sql=sql, params=params)
        return RecordScalar(headings=headings, data=data)
