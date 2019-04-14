"""Define abstractions."""

from .sql_tools import (
    _bind_sql,
    _load_connection,
    _get_results,
)


def execute_sql(con_name, sql, params=None):
    """Execute <sql> on <con>, with named <params>."""
    # bind the named parameters
    bound_sql = _bind_sql(sql, params)

    # load the connection
    connection, transaction = _load_connection(con_name)

    # execute the query, and rollback on error
    try:
        connection.execute(bound_sql)
        transaction.commit()

    except Exception as exception:
        transaction.rollback()
        raise exception

    finally:
        connection.close()


def recordset(con_name, sql, params=None):
    """
    Execute <sql> on <con>, with named <params>.

    Return (data, headings)
    """
    # bind the named parameters
    bound_sql = _bind_sql(sql, params)

    # load the connection
    connection, transaction = _load_connection(con_name)

    # get the results of the query
    data, headings = _get_results(connection, bound_sql)

    # commit and close the connection
    transaction.commit()
    connection.close()

    return data, headings
