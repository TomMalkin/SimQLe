"""Test the main Simqle class."""

import simqle


def test_init(mocker):
    # from simqle.mode_loader import mode_loader
    test_config = {"test key": "test value"}
    test_default_name = "test default name"

    # class MockedConfigLoader:
    # def __init__(self, file_name, mode):
    # self.config = test_config
    # self.default_connection_name = test_default_name

    mocked_mode_loader = mocker.patch(
        "simqle.simqle.mode_loader", autospec=True, return_value="testing"
    )

    mocker.patch.object(
        simqle.Simqle, attribute="_load_config", autospec=True, return_value=test_config
    )

    mocker.patch(
        "simqle.simqle.load_default_connection_name",
        autospec=True,
        return_value=test_default_name,
    )

    mocked_connection_manager = simqle.connection_manager.ConnectionManager(
        test_config,
        test_default_name,
    )

    mocker.patch.object(
        simqle.Simqle,
        attribute="_load_connection_manager",
        autospec=True,
        return_value=mocked_connection_manager,
    )

    mocker.patch("simqle.simqle.DatabaseActioner.__init__", return_value=None)

    # mocked_connection_manager = mocker.patch("simqle.simqle.ConnectionManager", autospec=True)
    # mocked_actioner = mocker.patch("simqle.simqle.DatabaseActioner", autospec=True)

    sq = simqle.Simqle(src="test source")

    assert sq.mode == "testing"
    assert sq.config == test_config
    assert sq.default_connection_name == test_default_name
    assert sq.connection_manager is mocked_connection_manager
    assert isinstance(sq.actioner, simqle.actioner.DatabaseActioner)


def test_load_connection_manager_method2(mocker, mocked_simqle, mocked_connection_manager):

    test_config = {"some": "config"}
    test_name = "some name"

    mocker.patch("simqle.simqle.ConnectionManager", new=mocked_connection_manager)
    mocker.patch("simqle.simqle.Simqle", new=mocked_simqle(test_config, test_name))

    sq = simqle.simqle.Simqle(src="some src", mode_override="some override")

    loaded_connection_manager = sq._load_connection_manager()

    assert loaded_connection_manager.config == test_config
    assert loaded_connection_manager._default_connection_name == test_name


def test_execute_sql_method(mocker, mocked_simqle, mocked_connection_manager):
    test_config = {"some": "config"}
    test_name = "some name"
    test_connection = "some connection"
    test_sql = "some sql"
    test_params = {"some": "params"}
    test_reference = "some reference"
    test_con_name = "some con name"

    mocker.patch("simqle.simqle.Simqle", new=mocked_simqle(test_config, test_name))
    mocker.patch("simqle.simqle.ConnectionManager", new=mocked_connection_manager)

    sq = simqle.simqle.Simqle(src="some src", mode_override="some override")

    assert sq.connection_manager.config == "test config"

    mocked_get_connection = mocker.patch.object(
        sq.connection_manager,
        "get_connection",
        autospec=True,
        return_value=test_connection,
    )

    mocked_execute_sql = mocker.patch.object(sq.actioner, "execute_sql", autospec=True)

    sq.execute_sql(
        sql=test_sql,
        con_name=test_con_name,
        params=test_params,
        reference=test_reference,
    )

    mocked_execute_sql.assert_called_once_with(
        connection=test_connection, sql=test_sql, params=test_params, reference=test_reference,
    )
    mocked_get_connection.assert_called_once_with(con_name=test_con_name)


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


def test_recordset_method(mocker):
    class MockedConnection(simqle.connection.Connection):
        def __init__(self):
            self.name = "test connection"

    test_connection = MockedConnection()

    mocked_get_connection = lambda self, con_name: test_connection

    mocker.patch.object(
        simqle.simqle.ConnectionManager, "get_connection", new=mocked_get_connection
    )

    mocked_recordset = mocker.patch.object(
        simqle.actioner.DatabaseActioner, "recordset", autospec=True
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
    sq.recordset(test_sql)

    mocked_recordset.assert_called_once_with(
        sq.actioner,
        connection=test_connection,
        sql=test_sql,
        params=None,
        reference=None,
    )


def test_record_method(mocker):
    class MockedConnection(simqle.connection.Connection):
        def __init__(self):
            self.name = "test connection"

    test_connection = MockedConnection()

    mocked_get_connection = lambda self, con_name: test_connection

    mocker.patch.object(
        simqle.simqle.ConnectionManager, "get_connection", new=mocked_get_connection
    )

    mocked_record = mocker.patch.object(simqle.actioner.DatabaseActioner, "record", autospec=True)

    class MockedConnectionManager(simqle.simqle.ConnectionManager):
        def __init__(self):
            pass

    class MockedSimqle(simqle.Simqle):
        def __init__(self):
            self.actioner = simqle.actioner.DatabaseActioner()
            self.connection_manager = MockedConnectionManager()

    sq = MockedSimqle()

    test_sql = "test sql"
    sq.record(test_sql)

    mocked_record.assert_called_once_with(
        sq.actioner,
        connection=test_connection,
        sql=test_sql,
        params=None,
        reference=None,
    )


def test_record_scalar_method(mocker):
    class MockedConnection(simqle.connection.Connection):
        def __init__(self):
            self.name = "test connection"

    test_connection = MockedConnection()

    mocked_get_connection = lambda self, con_name: test_connection

    mocker.patch.object(
        simqle.simqle.ConnectionManager, "get_connection", new=mocked_get_connection
    )

    mocked_record_scalar = mocker.patch.object(
        simqle.actioner.DatabaseActioner, "record_scalar", autospec=True
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
    sq.record_scalar(test_sql)

    mocked_record_scalar.assert_called_once_with(
        sq.actioner,
        connection=test_connection,
        sql=test_sql,
        params=None,
        reference=None,
    )
