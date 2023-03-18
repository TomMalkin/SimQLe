"""Define a Connection class which represents a connection to a named database."""

from urllib.parse import quote_plus

from sqlalchemy import create_engine


class Connection:  # pylint: disable=too-few-public-methods
    """The Connection class."""

    def __init__(self, config):
        """Create a new Connection from a config dict."""
        self.driver = config["driver"]
        self.name = config["name"]

        # for Microsoft ODBC connections, for example, the connection string must be url escaped. We
        # do this for the user if the url_escape option is True. See here for example and more info:
        # https://docs.sqlalchemy.org/en/13/dialects/mssql.html #pass-through-exact-pyodbc-string
        if "url_escape" in config:
            self.connection_string = quote_plus(config["connection"])
        else:
            self.connection_string = config["connection"]

        self.engine = create_engine(self.driver + self.connection_string)
