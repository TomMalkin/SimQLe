"""Tools to assist with sql."""

from sqlalchemy.sql import text, bindparam
from sqlalchemy.types import VARCHAR
from .connections import get_connection


def _bind_params(bound_sql, params):
    """Bind named parameters to the given sql."""
    for key, value in params.items():
        if isinstance(value, str):
            bound_sql = bound_sql.bindparams(
                bindparam(key=key,
                          value=value,
                          type_=VARCHAR(None))
            )
        else:
            bound_sql = bound_sql.bindparams(
                bindparam(key=key,
                          value=value)
            )
    return bound_sql


def _bind_sql(sql, params):
    bound_sql = text(sql)  # convert to the useful sqlalchemy text

    if params:  # add the named parameters
        bound_sql = _bind_params(bound_sql, params)

    return bound_sql


def _load_connection(con_name):
    con = get_connection(con_name)
    connection = con.connect()
    transaction = connection.begin()

    return connection, transaction


def _get_results(connection, bound_sql):
    result = connection.execute(bound_sql)
    data = result.fetchall()
    headings = result.keys()
    return data, headings
