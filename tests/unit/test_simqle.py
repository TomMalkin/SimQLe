"""Test the main Simqle class."""

import simqle


def test_init(mocker):
    # from simqle.mode_loader import mode_loader
    test_config = {"test key": "test value"}
    test_default_name = "test default name"

    mocker.patch(
        "simqle.simqle.mode_loader",
        autospec=True,
        return_value="testing",
    )

    mocker.patch.object(
        simqle.Simqle,
        attribute="_load_config",
        autospec=True,
        return_value=test_config,
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

    sq = simqle.Simqle(src="test source")

    assert sq.mode == "testing"
    assert sq.config == test_config
    assert sq.default_connection_name == test_default_name
    assert sq.connection_manager is mocked_connection_manager
    assert isinstance(sq.actioner, simqle.actioner.DatabaseActioner)


def test_load_connection_manager_method(mocker, mocked_simqle, mocked_connection_manager):

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
        connection=test_connection,
        sql=test_sql,
        params=test_params,
        reference=test_reference,
    )
    mocked_get_connection.assert_called_once_with(con_name=test_con_name)


def test_recordset_method(mocker, mocked_simqle, mocked_connection_manager):
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

    mocked_recordset = mocker.patch.object(sq.actioner, "recordset", autospec=True)

    sq.recordset(
        sql=test_sql,
        con_name=test_con_name,
        params=test_params,
        reference=test_reference,
    )

    mocked_recordset.assert_called_once_with(
        connection=test_connection,
        sql=test_sql,
        params=test_params,
        reference=test_reference,
    )
    mocked_get_connection.assert_called_once_with(con_name=test_con_name)


def test_record_method(mocker, mocked_simqle, mocked_connection_manager):
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

    mocked_record = mocker.patch.object(sq.actioner, "record", autospec=True)

    sq.record(
        sql=test_sql,
        con_name=test_con_name,
        params=test_params,
        reference=test_reference,
    )

    mocked_record.assert_called_once_with(
        connection=test_connection,
        sql=test_sql,
        params=test_params,
        reference=test_reference,
    )
    mocked_get_connection.assert_called_once_with(con_name=test_con_name)


def test_record_scalar_method(mocker, mocked_simqle, mocked_connection_manager):
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

    mocked_record_scalar = mocker.patch.object(sq.actioner, "record_scalar", autospec=True)

    sq.record_scalar(
        sql=test_sql,
        con_name=test_con_name,
        params=test_params,
        reference=test_reference,
    )

    mocked_record_scalar.assert_called_once_with(
        connection=test_connection,
        sql=test_sql,
        params=test_params,
        reference=test_reference,
    )
    mocked_get_connection.assert_called_once_with(con_name=test_con_name)


def test_load_config_method(mocker, mocked_config_loader, mocked_simqle):
    test_config = {"some": "config"}
    test_name = "some name"

    mocker.patch("simqle.simqle.ConfigLoader", new=mocked_config_loader(config=test_config))
    mocker.patch("simqle.simqle.Simqle", new=mocked_simqle(test_config, test_name))

    sq = simqle.simqle.Simqle(src="some src", mode_override="some override")

    config_loader = sq._load_config(src="some src", mode="some mode")

    assert config_loader == test_config


