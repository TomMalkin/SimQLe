"""Define pytest fixtures."""

import pytest
from simqle import Simqle
from simqle.actioner import DatabaseActioner, Transaction
from simqle.connection import Connection
from simqle.connection_manager import ConnectionManager
from simqle.timer import Timer


@pytest.fixture()
def mocked_timer():
    def mocked_timer_getter(elapsed_time=2):
        class MockedTimer(Timer):
            def __init__(self):
                pass

            def get_elapsed_time(self):
                return elapsed_time

        return MockedTimer

    return mocked_timer_getter


@pytest.fixture()
def mocked_transaction(mocked_connection):
    class MockedTransaction(Transaction):
        def __init__(self, connection=mocked_connection):
            self.connection = connection
            print("something")

    def __eq__(self, other):
        return isinstance(other, MockedTransaction)

    def __ne__(self, other):
        return not isinstance(other, MockedTransaction)

    return MockedTransaction


@pytest.fixture()
def mocked_connection():
    class MockedTransaction:
        def __init__(self):
            self.transaction = mocked_transaction()

        def rollback(self):
            self.transaction.rollback()

    class MockedConnectedEngine:
        def begin(self):
            return MockedTransaction()

    class MockedEngine:
        def connect(self):
            return MockedConnectedEngine()

    class MockedConnection(Connection):
        def __init__(self, config={"some": "config"}):
            self.config = config
            self.name = "test name"
            self.driver = "test driver"
            self.engine = MockedEngine()

    return MockedConnection


@pytest.fixture()
def generic_exception():
    class GenericException(Exception):
        pass

    return GenericException


@pytest.fixture()
def example_configuration():
    """An example config that can be used for testing."""
    config = {
        "default": "connection1",
        "connections": [
            {
                "name": "connection1",
                "driver": "sqlite:///",
                "connection": "/connection1.db",
                "url_escape": True,
            },
            {
                "name": "connection2",
                "driver": "sqlite:///",
                "connection": "/connection2.db",
            },
        ],
        "dev-connections": [
            {
                "name": "connection1",
                "driver": "sqlite:///",
                "connection": "/dev-connection1.db",
                "url_escape": True,
            },
            {
                "name": "connection2",
                "driver": "sqlite:///",
                "connection": "/dev-connection2.db",
            },
        ],
        "test-connections": [
            {
                "name": "connection1",
                "driver": "sqlite:///",
                "connection": "/test-connection1.db",
                "url_escape": True,
            },
            {
                "name": "connection2",
                "driver": "sqlite:///",
                "connection": "/test-connection2.db",
            },
        ],
    }
    return config


@pytest.fixture()
def example_configuration_with_no_default():
    """Return an example config that can be used for testing with no default."""
    config = {
        "dev-connections": [
            {
                "name": "connection1",
                "driver": "sqlite:///",
                "connection": "/connection1.db",
                "url_escape": True,
            },
            {
                "name": "connection2",
                "driver": "sqlite:///",
                "connection": "/connection2.db",
            },
        ]
    }
    return config
