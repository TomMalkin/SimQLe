import pytest
from simqle import Simqle
from simqle.actioner import DatabaseActioner, Transaction
from simqle.config_loader import ConfigLoader, ConfigValidator
from simqle.connection import Connection
from simqle.connection_manager import ConnectionManager
from simqle.container import Record, RecordScalar, RecordSet
from simqle.timer import Timer


@pytest.fixture()
def mocked_simqle(mocked_database_actioner, mocked_connection_manager):
    def mocked_simqle_getter(config, default_connection_name):
        class MockedSimqle(Simqle):
            def __init__(self, src=None, mode_override=None):
                self.src = src or "test src"
                self.mode_override = mode_override or "test mode_override"

                self.config = config
                self.default_connection_name = default_connection_name

                self.actioner = mocked_database_actioner()
                self.connection_manager = mocked_connection_manager()

        return MockedSimqle

    return mocked_simqle_getter


@pytest.fixture()
def mocked_connection_manager():
    class MockedConnectionManager(ConnectionManager):
        def __init__(self, config=None, default_connection_name=None):
            self.config = config or "test config"
            self._default_connection_name = default_connection_name or "test name"

    return MockedConnectionManager


@pytest.fixture()
def mocked_database_actioner():
    class MockedDatabaseActioner(DatabaseActioner):
        def __init__(self):
            pass

    return MockedDatabaseActioner


@pytest.fixture()
def mocked_config_loader():
    def mocked_config_loader_getter(config):
        class MockedConfigLoader(ConfigLoader):
            def __init__(self, src, mode):
                self.src = src
                self.mode = mode
                self._config = config

        return MockedConfigLoader

    return mocked_config_loader_getter


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
        def __init__(self, connection=mocked_connection()):
            self.connection = connection
            print("something")

    def __eq__(self, other):
        return isinstance(other, MockedTransaction)

    def __ne__(self, other):
        return not isinstance(other, MockedTransaction)

    return MockedTransaction


@pytest.fixture()
def mocked_connection():
    class MockedConnection(Connection):
        def __init__(self, config={"some": "config"}):
            self.config = config
            self.name = "test name"
            self.driver = "test driver"
            self._engine = "test engine"

    return MockedConnection


@pytest.fixture()
def generic_exception():
    class GenericException(Exception):
        pass

    return GenericException

@pytest.fixture()
def mocked_config_validator():
    class MockedConfigValidator(ConfigValidator):
        def __init__(self, config):
            self.config = config
    return MockedConfigValidator


@pytest.fixture()
def mocked_config_loader():
    class MockedConfigLoader(ConfigLoader):
        def __init__(self, src, mode):
            self.src = src
            self.mode = mode
    return MockedConfigLoader


