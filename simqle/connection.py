class Connection:
    """
    The _Connection class.

    This represents a single connection. This class also manages the execution of SQL, including the
    management of transactions.

    The engine is lazily loaded the first time either execute_sql or recordset is called.

    This class shouldn't be loaded outside the ConnectionManager class, and so is marked as internal
    only.
    """

    def __init__(self, conn_config):
        """Create a new Connection from a config dict."""
        self.driver = conn_config["driver"]
        self._engine = None
        self.name = conn_config["name"]

        # Edit the connection based on configuration options.

        # for Microsoft ODBC connections, for example, the connection string
        # must be url escaped. We do this for the user if the url_escape
        # option is True. See here for example and more info:
        # https://docs.sqlalchemy.org/en/13/dialects/mssql.html
        #   #pass-through-exact-pyodbc-string
        if "url_escape" in conn_config:
            self.connection_string = quote_plus(conn_config["connection"])
        else:
            self.connection_string = conn_config["connection"]

        # self.id = uuid.uuid4
        # log.info(f"Connection created for {conn_config['name']} with id "
        #          f"{self.id}")

    def _connect(self):
        """Create an engine based on sqlalchemy's create_engine."""
        self._engine = create_engine(self.driver + self.connection_string)

    @property
    def engine(self):
        """Load the engine if it hasn't been loaded before."""
        if not self._engine:
            self._connect()

        return self._engine

    def execute_sql(self, sql, params=None):
        """Execute :sql: on this connection with named :params:."""
        bound_sql = bind_sql(sql, params)

        connection = self.engine.connect()
        transaction = connection.begin()

        # execute the query, and rollback on error
        try:
            connection.execute(bound_sql)
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            connection.close()

    def recordset(self, sql, params=None):
        """
        Execute <sql> on <con>, with named <params>.

        Return (headings, data)
        """
        # bind the named parameters.
        bound_sql = bind_sql(sql, params)

        connection = self.engine.connect()
        transaction = connection.begin()

        try:
            result = connection.execute(bound_sql)
            data = result.fetchall()
            headings = list(result.keys())
            transaction.commit()

        except Exception as exception:
            transaction.rollback()
            raise exception

        finally:
            connection.close()

        return headings, data
