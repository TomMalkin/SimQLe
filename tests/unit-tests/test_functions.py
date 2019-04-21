"""Test the functions.py module."""


def test_execute_sql(monkeypatch):
    """Test the execute_sql function."""
    monkeypatch.setattr("simqle.functions._bind_sql",
                        lambda sql, params: sql)

    monkeypatch.setattr("simqle.functions._load_connection",
                        lambda con_name: ("", ""))
