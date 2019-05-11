"""Test connections.py."""

from simqle import connections


def test_load_connections(monkeypatch, make_fake_load_yaml_from_file):
    """Test the load_connections functions."""
    monkeypatch.setattr("simqle.connections._load_yaml_from_file",
                        make_fake_load_yaml_from_file)

    monkeypatch.setattr("simqle.connections.create_engine",
                        lambda x: x)

    monkeypatch.setattr("simqle.connections.quote_plus",
                        lambda x: x)

    connections.reset_connections()
    assert connections.CONNS == {}

    connections.load_connections()

    connection = ("DRIVER={SQL Server};"
                  "UID=<username>;"
                  "PWD=<password>;"
                  "SERVER=<my-server>")

    assert connections.CONNS == {
        "fake database": "mssql+pyodbc:///?odbc_connect=" + connection,
        "fake database 2": "mssql2+pyodbc:///?odbc_connect=" + connection
        }


def test_get_connection():
    """Test the get_connection function."""
    _CONNS = connections.CONNS

    test_key = list(_CONNS.keys())[0]
    assert connections.get_connection(test_key) == connections.CONNS[test_key]
