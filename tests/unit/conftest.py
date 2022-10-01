from simqle import Simqle
from simqle.container import RecordSet, Record, RecordScalar
from simqle.connection import Connection
from simqle.connection_manager import ConnectionManager
from simqle.actioner import DatabaseActioner
import pytest

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

# class TestRecordSet(RecordSet):
    # def __init__(self, headings, data):
        # self.headings = headings
        # self.data = data


# class TestRecord(Record):
    # def __init__(self, headings, data):
        # self.headings = headings
        # self.data = data


# class TestRecordScalar(RecordScalar):
    # def __init__(self, headings, data):
        # self.headings = headings
        # self.data = data


# @pytest.fixture()
# def get_connection_manager_mock(mocker, test_config):
    # """Yield an initiliased connection manager with basic settings as a mock."""

    # mocker.patch.object(ConnectionManager, "_get_mode", new=lambda self: "production")
    # mocker.patch.object(ConnectionManager, "_get_mode_name", new=lambda self, mode: "connections")

    # mocker.patch.object(ConnectionManager, "_load_config", new=lambda self, file_name: test_config)

    # mocker.patch.object(ConnectionManager, "_load_default_connection", new=lambda self: None)

    # # cm = ConnectionManager()

    # yield ConnectionManager

# @pytest.fixture()
# def get_connection_mock(mocker):
    # """Yield an initialised _Connection object with basic settings."""
    # class _TestConnection(_Connection):
        # def __init__(self):
            # self.driver = "test driver"
            # self._engine = None
            # self.name = "test name"
            # self.connection_string = "test connection string"

    # yield _TestConnection



# @pytest.fixture()
# def get_recordset_mock(mocker):
    # mocker.patch("simqle.recordset.RecordSet")
    # yield RecordSet


# @pytest.fixture()
# def get_record_mock(mocker):
    # mocker.patch(Record, new=TestRecord)
    # yield Record


# @pytest.fixture()
# def get_record_scalar_mock(mocker):
    # mocker.patch(RecordScalar, new=TestRecordScalar)
    # yield RecordScalar


# @pytest.fixture()
# def test_config():
    # yield {"example": "config"}
