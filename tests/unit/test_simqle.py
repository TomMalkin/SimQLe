"""Test the main Simqle class."""

import simqle


def test_import():
    from simqle import Simqle


def test_init(mocker):
    # from simqle.mode_loader import mode_loader
    test_config = {"test key": "test value"}
    test_default_name = "test default name"

    class MockedConfigLoader:
        def __init__(self, file_name, mode):
            self.config = test_config
            self.default_connection_name = test_default_name

    mocked_mode_loader = mocker.patch("simqle.simqle.mode_loader", autospec=True)
    mocked_config_loader = mocker.patch("simqle.simqle.ConfigLoader", new=MockedConfigLoader)
    mocked_connection_manager = mocker.patch("simqle.simqle.ConnectionManager", autospec=True)
    mocked_actioner = mocker.patch("simqle.simqle.DatabaseActioner", autospec=True)

    sq = simqle.Simqle()

    mocked_mode_loader.assert_called_once()
    mocked_connection_manager.assert_called_once_with(
        config=test_config,
        default_connection_name=test_default_name,
    )

    mocked_actioner.assert_called_once()

    assert sq.config == test_config
    assert sq.default_connection_name == test_default_name


# def test_execute_sql_method(mocker):
# mocked_connection_class = mocker.patch("simqle.connection.Connection", autospec=True)
# mocked_connection = mocked_connection_class(con_config={"test": "value"})

# mocked_get_connection = lambda self, con_name: mocked_connection
# mocker.patch.object(simqle.simqle.ConnectionManager, "get_connection", new=mocked_get_connection)

# mocked_execute_sql = mocker.patch.object(simqle.actioner.DatabaseActioner, "execute_sql", autospec=True)

# class MockedConnectionManager(simqle.simqle.ConnectionManager):
# def __init__(self):
# pass

# class MockedSimqle(simqle.Simqle):
# def __init__(self):
# self.actioner = simqle.actioner.DatabaseActioner()
# self.connection_manager = MockedConnectionManager()

# sq = MockedSimqle()

# test_sql = "test sql"
# sq.execute_sql(test_sql)

# # mocked_connection.assert_called_once()
# mocked_execute_sql.assert_called_once_with(connection=mocked_connection, sql=test_sql,
# params=None, reference=None)


def test_execute_sql_method(mocker):
    class MockedConnection(simqle.connection.Connection):
        def __init__(self):
            self.name = "test connection"

    test_connection = MockedConnection()

    mocked_get_connection = lambda self, con_name: test_connection

    mocker.patch.object(
        simqle.simqle.ConnectionManager, "get_connection", new=mocked_get_connection
    )

    mocked_execute_sql = mocker.patch.object(
        simqle.actioner.DatabaseActioner, "execute_sql", autospec=True
    )

    class MockedConnectionManager(simqle.simqle.ConnectionManager):
        def __init__(self):
            pass

    class MockedSimqle(simqle.Simqle):
        def __init__(self):
            self.actioner = simqle.actioner.DatabaseActioner()
            self.connection_manager = MockedConnectionManager()

    sq = MockedSimqle()

    test_sql = "test sql"
    sq.execute_sql(test_sql)

    mocked_execute_sql.assert_called_once_with(
        sq.actioner,
        connection=test_connection,
        sql=test_sql,
        params=None,
        reference=None,
    )


def test_recordset_method(mocker):
    pass


def test_record_method(mocker):
    pass


def test_record_scalar_method(mocker):
    pass
