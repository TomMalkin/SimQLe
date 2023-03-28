"""Test the ConnectionManager class."""

from pytest import raises
from simqle.connection_manager import ConnectionManager
from simqle.exceptions import NoDefaultConnectionError, UnknownConnectionError


def test_init(mocker, example_configuration, mocked_connection):
    """Test the initialisation of ConnectionManager."""
    section_config = example_configuration.get("dev-connections")

    mocker.patch("simqle.connection_manager.Connection", new=mocked_connection)
    con_man = ConnectionManager(config=section_config, default_connection_name="connection1")
    assert con_man.config == section_config


def test_default_connection(mocker, example_configuration, mocked_connection):
    """Test the default connection property."""
    section_config = example_configuration.get("dev-connections")
    mocker.patch("simqle.connection_manager.Connection", new=mocked_connection)
    con_man = ConnectionManager(config=section_config, default_connection_name="connection1")
    assert con_man.default_connection_name == "connection1"


def test_missing_default_connection():
    """Test that an error is raised if no default connection exists and is accessed."""
    con_man = ConnectionManager(config={})

    with raises(NoDefaultConnectionError):
        _ = con_man.default_connection_name


def test_get_connection_method(mocker, example_configuration, mocked_connection):

    section_config = example_configuration.get("dev-connections")
    mocker.patch("simqle.connection_manager.Connection", new=mocked_connection)
    cm = ConnectionManager(config=section_config, default_connection_name="connection1")
    assert cm.connections["connection2"] == cm.get_connection("connection2")
    assert cm.connections["connection1"] == cm.get_connection()
    with raises(UnknownConnectionError):
        cm.get_connection("Wrong Connection Name")




def test_get_engine_method(mocker, example_configuration, mocked_connection):
    section_config = example_configuration.get("dev-connections")
    mocker.patch("simqle.connection_manager.Connection", new=mocked_connection)
    cm = ConnectionManager(config=section_config)

    assert cm.get_engine("connection1") == cm.connections["connection1"].engine
