"""Define a Connection class which represents a connection to a named database."""

from urllib.parse import quote_plus

from sqlalchemy import create_engine


class Connection:
    """
    The _Connection class.

    This represents a single connection. This class also manages the execution of SQL, including the
    management of transactions.

    The engine is lazily loaded the first time either execute_sql or recordset is called.

    This class shouldn't be loaded outside the ConnectionManager class, and so is marked as internal
    only.
    """

    def __init__(self, con_config):
        """Create a new Connection from a config dict."""
        self.driver = con_config["driver"]
        self._engine = None
        self.name = con_config["name"]

        # Edit the connection based on configuration options.

        # for Microsoft ODBC connections, for example, the connection string
        # must be url escaped. We do this for the user if the url_escape
        # option is True. See here for example and more info:
        # https://docs.sqlalchemy.org/en/13/dialects/mssql.html
        #   #pass-through-exact-pyodbc-string
        if "url_escape" in con_config:
            self.connection_string = quote_plus(con_config["connection"])
        else:
            self.connection_string = con_config["connection"]

    @property
    def engine(self):
        """Load the engine if it hasn't been loaded before."""
        if not self._engine:
            self._engine = create_engine(self.driver + self.connection_string)

        return self._engine

    def connect(self):
        return self._engine.connect()
