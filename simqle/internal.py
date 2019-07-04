"""Internal ConnectionManager."""

from simqle.connection_manager import ConnectionManager

INTERNAL_CONNECTION_MANAGER = None


def load_connections(connections_file="./.connections.yaml"):
    """Load the Internal connection manager."""
    global INTERNAL_CONNECTION_MANAGER

    # if INTERNAL_CONNECTION_MANAGER:
    #     raise Exception("The internal connection manager has already been "
    #                     "loaded, this would overwrite the current one.")
    # TODO: add load details to the ConnectionManager class so we can tell
    # the user at this point what module loaded the internal simqle
    # ConnectionManager instance.

    INTERNAL_CONNECTION_MANAGER = ConnectionManager(file_name=connections_file)


def execute_sql(con_name, sql, params=None):
    """Execute sql on the Internal ConnectionManager."""
    INTERNAL_CONNECTION_MANAGER.execute_sql(sql=sql, con_name=con_name,
                                            params=params)


def recordset(con_name, sql, params=None):
    """Return SQL results from the Internal ConnectionManager."""
    return INTERNAL_CONNECTION_MANAGER.recordset(sql, con_name, params=params)


def get_connection(con_name):
    """Return a connection engine from the Internal ConnectionManager."""
    return INTERNAL_CONNECTION_MANAGER.get_engine(con_name)


def get_engine(con_name):
    """Return a connection engine from the Internal ConnectionManager."""
    return INTERNAL_CONNECTION_MANAGER.get_engine(con_name)


def reset_connections():
    """Clear the internal ConnectionManager's connections."""
    if INTERNAL_CONNECTION_MANAGER:  # TODO: add __bool__ to ConnectionManager
        INTERNAL_CONNECTION_MANAGER.reset_connections()
