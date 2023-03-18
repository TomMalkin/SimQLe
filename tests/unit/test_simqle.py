"""Test the main Simqle class."""

import simqle
from pytest import raises


def test_init(mocker, example_configuration):
    """Test the initilisation of a Simqle class with a filename."""
    mocker.patch("os.getenv", return_value="development")

    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration,
    )

    test_simqle = simqle.Simqle(file_name="./.connections.yaml")

    assert test_simqle.file_name == "./.connections.yaml"
    assert test_simqle.mode == "development"
    assert test_simqle.section == "dev-connections"
    assert test_simqle.full_config == example_configuration
    assert test_simqle.config == example_configuration.get("dev-connections")
    assert test_simqle.default_connection_name == "connection1"


def test_init_mode_override(mocker, example_configuration):
    """Test the mode override option."""
    mocker.patch("os.getenv", return_value="development")

    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration,
    )

    # os.getenv will return "development", but we're overriding using "production"
    test_simqle = simqle.Simqle(file_name="./.connections.yaml", mode_override="production")

    assert test_simqle.file_name == "./.connections.yaml"
    assert test_simqle.mode == "production"
    assert test_simqle.section == "connections"
    assert test_simqle.full_config == example_configuration
    assert test_simqle.config == example_configuration.get("connections")
    assert test_simqle.default_connection_name == "connection1"


def test_from_dict_class_method(mocker, example_configuration):
    """Test that the class can be created from the from_dict classmethod."""
    mocker.patch("os.getenv", return_value="development")

    # create the simqle class using the from_dict classmethod
    test_simqle = simqle.Simqle.from_dict(config_dict=example_configuration)

    assert test_simqle.file_name is None
    assert test_simqle.mode == "development"
    assert test_simqle.section == "dev-connections"
    assert test_simqle.full_config == example_configuration
    assert test_simqle.config == example_configuration.get("dev-connections")
    assert test_simqle.default_connection_name == "connection1"


def test_missing_section(mocker):
    """Test that if the section is missing then an error is rasied."""
    mocker.patch("os.getenv", return_value="not a mode")

    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value={},
    )

    with raises(ValueError):
        _ = simqle.Simqle(file_name="./.connections.yaml")


def test_init_with_no_default(mocker, example_configuration_with_no_default):
    """Test the initilisation of a Simqle class with a filename."""
    mocker.patch("os.getenv", return_value="development")

    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration_with_no_default,
    )

    test_simqle = simqle.Simqle(file_name="./.connections.yaml")

    assert test_simqle.default_connection_name is None


def test_load_config_from_file(mocker, example_configuration):
    """Test loading a config from a file."""
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("simqle.simqle.safe_load", return_value=example_configuration)

    config = simqle.Simqle.load_config_from_file(file_name="examplefile")

    assert config == example_configuration


def test_load_config_from_file_missing(mocker):
    """Test loading a config from a file that doesn't exist."""
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("simqle.simqle.safe_load", side_effect=FileNotFoundError())

    with raises(FileNotFoundError):
        _ = simqle.Simqle.load_config_from_file(file_name="examplefile")


def test_execute_sql_method(mocker, example_configuration, mocked_connection):
    """Test the execute_sql method."""
    mocker.patch("os.getenv", return_value="development")
    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration,
    )

    mocker.patch.object(
        simqle.simqle.ConnectionManager,
        attribute="get_connection",
        return_value=mocked_connection,
    )
    mocker.patch.object(
        simqle.simqle.DatabaseActioner,
        attribute="execute_sql",
    )

    test_simqle = simqle.Simqle(file_name="./.connections.yaml")

    test_simqle.execute_sql(sql="some_sql")

    test_simqle.actioner.execute_sql.assert_called_once()


def test_recordset_method(mocker, example_configuration, mocked_connection):
    """Test the recordset method."""
    mocker.patch("os.getenv", return_value="development")
    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration,
    )

    test_connection = mocker.patch.object(
        simqle.simqle.ConnectionManager,
        attribute="get_connection",
        return_value=mocked_connection,
    )
    mocker.patch.object(
        simqle.simqle.DatabaseActioner,
        attribute="recordset",
    )

    test_simqle = simqle.Simqle(file_name="./.connections.yaml")

    test_simqle.recordset(sql="some_sql")

    test_simqle.actioner.recordset.assert_called_once()


def test_record_method(mocker, example_configuration, mocked_connection):
    """Test the recordset method."""
    mocker.patch("os.getenv", return_value="development")
    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration,
    )

    mocker.patch.object(
        simqle.simqle.ConnectionManager,
        attribute="get_connection",
        return_value=mocked_connection,
    )
    mocker.patch.object(
        simqle.simqle.DatabaseActioner,
        attribute="record",
    )

    test_simqle = simqle.Simqle(file_name="./.connections.yaml")

    test_simqle.record(sql="some_sql")

    test_simqle.actioner.record.assert_called_once()


def test_record_scalar_method(mocker, example_configuration, mocked_connection):
    """Test the record_scalarset method."""
    mocker.patch("os.getenv", return_value="development")
    mocker.patch.object(
        simqle.Simqle,
        attribute="load_config_from_file",
        autospec=True,
        return_value=example_configuration,
    )

    mocker.patch.object(
        simqle.simqle.ConnectionManager,
        attribute="get_connection",
        return_value=mocked_connection,
    )
    mocker.patch.object(
        simqle.simqle.DatabaseActioner,
        attribute="record_scalar",
    )

    test_simqle = simqle.Simqle(file_name="./.connections.yaml")

    test_simqle.record_scalar(sql="some_sql")

    test_simqle.actioner.record_scalar.assert_called_once()
