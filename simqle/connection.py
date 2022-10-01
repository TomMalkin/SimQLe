"""Define a Connection class which represents a connection to a named database."""

from urllib.parse import quote_plus

from sqlalchemy import create_engine


class Connection:
    """
    The Connection class.

    This represents a single connection. The engine is lazily loaded the first time either
    execute_sql or recordset is called.
    """

    def __init__(self, config):
        """Create a new Connection from a config dict."""
        self.driver = config["driver"]
        self._engine = None
        self.name = config["name"]

        # for Microsoft ODBC connections, for example, the connection string must be url escaped. We
        # do this for the user if the url_escape option is True. See here for example and more info:
        # https://docs.sqlalchemy.org/en/13/dialects/mssql.html #pass-through-exact-pyodbc-string
        if "url_escape" in config:
            self.connection_string = quote_plus(config["connection"])
        else:
            self.connection_string = config["connection"]

    @property
    def engine(self):
        """Get the engine, loading it if it hasn't been loaded before."""
        if not self._engine:
            self._engine = create_engine(self.driver + self.connection_string)

        return self._engine

    def connect(self):
        """Return the engine connection."""
        return self.engine.connect()
