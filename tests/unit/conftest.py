from simqle import ConnectionManager
from simqle.recordset import RecordSet, Record, RecordScalar
import pytest


class TestRecordSet(RecordSet):
    def __init__(self, headings, data):
        self.headings = headings
        self.data = data


class TestRecord(Record):
    def __init__(self, headings, data):
        self.headings = headings
        self.data = data


class TestRecordScalar(RecordScalar):
    def __init__(self, headings, data):
        self.headings = headings
        self.data = data


@pytest.fixture()
def get_connection_manager_mock(mocker, test_config):
    """Yield an initiliased connection manager with basic settings as a mock."""

    mocker.patch.object(ConnectionManager, "_get_mode", new=lambda self: "production")
    mocker.patch.object(ConnectionManager, "_get_mode_name", new=lambda self, mode: "connections")

    mocker.patch.object(ConnectionManager, "_load_config", new=lambda self, file_name: test_config)

    mocker.patch.object(ConnectionManager, "_load_default_connection", new=lambda self: None)

    # cm = ConnectionManager()

    yield ConnectionManager


@pytest.fixture()
def get_recordset_mock(mocker):
    mocker.patch("simqle.recordset.RecordSet")
    yield RecordSet


@pytest.fixture()
def get_record_mock(mocker):
    mocker.patch(Record, new=TestRecord)
    yield Record


@pytest.fixture()
def get_record_scalar_mock(mocker):
    mocker.patch(RecordScalar, new=TestRecordScalar)
    yield RecordScalar


@pytest.fixture()
def test_config():
    yield {"example": "config"}
