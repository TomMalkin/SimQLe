from simqle.connection_manager import ConnectionManager


class Provider:

    def __init__(self, connection_manager= None, config_file= None):

        if connection_manager is not None:
            self.connection_mananger = connection_manager

        else:
            if config_file is not None:
                self.connection_manager = ConnectionManager(config_file)
            else:
                raise Exception('Need a valid file!')


    def GetRecordSet(self, conn_name, sql_string, params= None):
        connection = self.connection_manager.GetConnection(conn_name)
        return connection.ExecuteSql(sql_string, params= params)



if __name__ == '__main__':

    ## COULD : be passed in via command args or an ENV variable
    CONFIG_FILE = 'tests/integration-tests/mysql-tests/.connections.yaml'

    provider = Provider(config_file= CONFIG_FILE)

    SQL_STRING = 'SELECT * FROM TBL1'

    record = provider.GetRecordSet('my-sqlite-database', SQL_STRING)

    print(record)
