"""
The Connections module.

The CONNS object stores our named sqlalchemy engines and is updated by the
load_connections function.
"""

from yaml import safe_load
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from .constants import DEV_MAP
import os

CONNS = {}


def load_connections(connections_file="./.connections.yaml"):
    """
    Load engines into the CONNS dict from the <connections_file>.

    <test> changes whether to load the test database strings.
    """
    connections_yaml = _load_yaml_from_file(connections_file)

    test_mode = os.getenv("SIMQLE_TEST", False)

    # load the set of connections based on test mode
    dev_type = DEV_MAP[test_mode]

    for connection in connections_yaml[dev_type]:

        name = connection["name"]
        driver = connection["driver"]

        # for Microsoft ODBC connections, for example, the connection string
        # must be url escaped. We do this for the user if the url_escape
        # option is True. See here for example and more info:
        # https://docs.sqlalchemy.org/en/13/dialects/mssql.html
        #   #pass-through-exact-pyodbc-string
        url_escape = connection.get("url_escape")
        if url_escape:
            connection_string = quote_plus(connection["connection"])
        else:
            connection_string = connection["connection"]

        # Our connection object is created through sqlalchemy's create_engine
        # function, and stored in the connection map CONNS.
        CONNS[name] = create_engine(driver + connection_string)


def get_connection(con_name):
    """Return the connection object defined by the given <name>."""
    return CONNS.get(con_name)


def _load_yaml_from_file(connections_file):
    with open(connections_file) as file:
        return safe_load(file.read())


def reset_connections():
    """Set the CONNS map to empty."""
    CONNS.clear()
