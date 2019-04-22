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

        # If the database connection is a file (for example, sqlite), then the
        # connection string is simply a path, and we don't want to run that
        # through the quote_plus parsing function.
        if connection.get("file"):
            connection_string = connection["connection"]
        else:
            connection_string = quote_plus(connection["connection"])

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
