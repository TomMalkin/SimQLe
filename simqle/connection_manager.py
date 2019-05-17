
from yaml import safe_load
from sqlalchemy import create_engine
from sqlalchemy.sql import text, bindparam
from sqlalchemy.types import VARCHAR
from urllib.parse import quote_plus


class ConnectionManager:

    def __init__(self, file_name):

        self.connections = {}
        self.config = self._LoadYamlFromFile(file_name)


    def _LoadYamlFromFile(self, connections_file):
        with open(connections_file) as file:
            return safe_load(file.read())


    def GetConnection(self, conn_name):

        if conn_name in self.connections:
            return self.connections[conn_name]

        for conn_config in self.config['connections']:
            if conn_config['name'] == conn_name:
                self.connections[conn_name] = Connection(conn_config)
                return self.connections[conn_name]


        raise Exception('Unknown connection %s' % conn_name)


class Connection:

    def __init__(self, conn_config):

        self.driver = conn_config['driver']

        if 'url_escape' in conn_config:
            self.connection_string = quote_plus(conn_config['connection'])
        else:
            self.connection_string = conn_config['connection']

        self.engine = None

    def Connect(self):
        self.engine = create_engine(self.driver + self.connection_string)


    def BindParams(self, sql_string, params):

        for key, value in params.items():
            if isinstance(value, str):
                bound_sql = bound_sql.bindparams(
                    bindparam(
                        key     = key,
                        value   = value,
                        type_   = VARCHAR(None)
                    )
                )
            else:
                bound_sql = bound_sql.bindparams(
                    bindparam(
                        key     = key,
                        value   = value
                    )
                )

    def BindSql(self, sql_string, params= None):

        bound_sql = text(sql_string)

        if params:
            bound_sql = self.BindParams(sql_string, params)

        return bound_sql


    def ExecuteSql(self, sql_string, params= None):

        if self.engine is None:
            self.Connect()

        conn = self.engine.connect()
        transaction = conn.begin()

        bound_sql = self.BindSql(sql_string, params= params)

        results = conn.execute(bound_sql)
        data = results.fetchall()
        headings = results.keys()

        transaction.commit()
        conn.close()

        return data, headings

