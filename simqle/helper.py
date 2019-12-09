from sqlalchemy import text, VARCHAR, bindparam


def bind_sql(sql, params):
    """
    Bind parameters to a SQL query.

    Useful if the library that is executing your query, for exaple pandas,
    doesn't like named parameters. bind_sql will return a sql query with the
    parameters bound to the query.

    Args:
        sql: The SQL query to bind parameters to
        params: The named parameters to bind to the query
    """
    bound_sql = text(sql)  # convert to the useful sqlalchemy text

    if params:
        for key, value in params.items():
            # If the type of the value of the parameter is str, then we use
            # the VARCHAR object with no maximum, else use the default Type
            type_ = VARCHAR(None) if isinstance(value, str) else None
            param = bindparam(key=key, value=value, type_=type_)
            bound_sql = bound_sql.bindparams(param)

    return bound_sql
