"""pytest fixtures for the unit tests."""

import pytest


@pytest.fixture
def fake_connection_string():
    return ("DRIVER={SQL Server};"
            "UID=<username>;"
            "PWD=<password>;"
            "SERVER=<my-server>")


@pytest.fixture
def fake_connections():
    """Return an example connection dictionary."""
    fake_connection = ("DRIVER={SQL Server};"
                       "UID=<username>;"
                       "PWD=<password>;"
                       "SERVER=<my-server>")

    fake_test_connection = ("DRIVER={SQL Server};"
                            "UID=<username>;"
                            "PWD=<password>;"
                            "SERVER=<my-server>")

    return {"connections": [{"name": "fake database",
                             "driver": "mssql+pyodbc:///?odbc_connect=",
                             "connection": fake_connection},
                            {"name": "fake database 2",
                             "driver": "mssql2+pyodbc:///?odbc_connect=",
                             "connection": fake_connection,
                             "url_escape": True}],
            "test-connections": [{"name": "fake test database",
                                  "driver": "mssql+pyodbc:///?odbc_connect=",
                                  "connection": fake_test_connection}]}


@pytest.fixture
def make_fake_load_yaml_from_file(fake_connections):
    """Return a fake _load_yaml_from_file."""
    def fake_load_yaml_from_file(connections_file):
        return fake_connections
    return fake_load_yaml_from_file
