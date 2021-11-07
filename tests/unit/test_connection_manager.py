"""Test the ConnectionManager class."""

from simqle.connection_manager import ConnectionManager


def test_connection_manager_init():
    test_config = {"some key": "some value"}
    test_class = ConnectionManager(config=test_config)
    assert test_class.config == test_config

def test_get_engine_method(mocker):
    pass


def test_get_connection_method(mocker):
    pass

def test_get_con_name_method(mocker):
    pass



