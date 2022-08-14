"""Test the DatabaseActioner class."""
import pytest
import simqle
from simqle.actioner import DatabaseActioner


def test_init():

    database_actioner = DatabaseActioner()
    assert isinstance(database_actioner, DatabaseActioner)


def test_execute_sql_method(mocker):

    mock_get_reference = lambda self, reference, sql: "test reference"
    mocker.patch.object(DatabaseActioner, "get_reference", new=mock_get_reference)

    mock_bind_sql = lambda sql, params: "bound sql"
    mocker.patch("simqle.actioner.bind_sql", new=mock_bind_sql)

    mocker.patch.object(simqle.timer.Timer, "get_elapsed_time", lambda self: 2)

    class MockedTransaction:
        def commit(self):
            pass

        def rollback(self):
            pass

    class MockedEngine:
        def begin(self):
            return MockedTransaction()

        def close(self):
            pass

        def execute(self, bound_sql):
            pass

    class MockedConnection(simqle.connection.Connection):
        def __init__(self):
            self.name = "test connection"

        def connect(self):
            return MockedEngine()

    mocker.patch.object(simqle.connection.Connection, "connect", new=lambda: MockedEngine())

    mocker.patch.object(MockedEngine, "execute", autospec=True)
    mocker.patch.object(MockedEngine, "close", autospec=True)
    mocker.patch.object(MockedTransaction, "commit", autospec=True)
    mocker.patch.object(MockedTransaction, "rollback", autospec=True)

    database_actioner = DatabaseActioner()

    # successful execution
    mocked_connection = MockedConnection()
    database_actioner.execute_sql(connection=mocked_connection, sql="test sql")

    MockedEngine.execute.assert_called_once()
    MockedTransaction.commit.assert_called_once()
    MockedEngine.close.assert_called_once()

    # if the transaction causes an error
    def mock_error_execute(self, bound_sql):
        raise ValueError()

    mocker.patch.object(MockedEngine, "execute", new=mock_error_execute)

    MockedTransaction.commit.reset_mock()
    MockedEngine.close.reset_mock()

    with pytest.raises(ValueError) as exc_info:
        database_actioner.execute_sql(connection=mocked_connection, sql="test sql")

    MockedTransaction.commit.assert_not_called()
    MockedTransaction.rollback.assert_called_once()
    MockedEngine.close.assert_called_once()


def test_get_data_method(mocker):
    mock_get_reference = lambda self, reference, sql: "test reference"
    mocker.patch.object(DatabaseActioner, "get_reference", new=mock_get_reference)

    mock_bind_sql = lambda sql, params: "bound sql"
    mocker.patch("simqle.actioner.bind_sql", new=mock_bind_sql)

    mocker.patch.object(simqle.timer.Timer, "get_elapsed_time", lambda self: 2)

    class MockedResult:
        def fetchall(self):
            return [("a", "b"), ("c", "d")]

        def keys(self):
            return ["h1", "h2"]

    class MockedTransaction:
        def commit(self):
            pass

        def rollback(self):
            pass

    class MockedEngine:
        def begin(self):
            return MockedTransaction()

        def close(self):
            pass

        def execute(self, bound_sql):
            return MockedResult()

    class MockedConnection(simqle.connection.Connection):
        def __init__(self):
            self.name = "test connection"

        def connect(self):
            return MockedEngine()

    mocker.patch.object(simqle.connection.Connection, "connect", new=lambda: MockedEngine())

    mocker.patch.object(MockedEngine, "close", autospec=True)
    mocker.patch.object(MockedTransaction, "commit", autospec=True)
    mocker.patch.object(MockedTransaction, "rollback", autospec=True)

    database_actioner = DatabaseActioner()

    # successful execution
    mocked_connection = MockedConnection()
    headings, data = database_actioner.get_data(connection=mocked_connection, sql="test sql")

    MockedTransaction.commit.assert_called_once()
    MockedEngine.close.assert_called_once()

    assert headings == ["h1", "h2"]
    assert data == [("a", "b"), ("c", "d")]

    # if the transaction causes an error
    def mock_error_execute(self, bound_sql):
        raise ValueError()

    mocker.patch.object(MockedEngine, "execute", new=mock_error_execute)

    MockedTransaction.commit.reset_mock()
    MockedEngine.close.reset_mock()

    with pytest.raises(ValueError) as exc_info:
        headings, data = database_actioner.get_data(connection=mocked_connection, sql="test sql")

    MockedTransaction.commit.assert_not_called()
    MockedTransaction.rollback.assert_called_once()
    MockedEngine.close.assert_called_once()


def test_recordset_method(mocker):

    test_headings = ["h1", "h2"]
    test_data = [("a", "b"), ("c", "d")]

    def mocked_get_data(self, connection, sql, params, reference):
        return test_headings, test_data

    class MockedRecordSet(simqle.actioner.RecordSet):
        def __init__(self, headings, data):
            self.headings = headings
            self.data = data

    mocker.patch.object(simqle.actioner.DatabaseActioner, "get_data", new=mocked_get_data)
    mocker.patch("simqle.actioner.RecordSet", new=MockedRecordSet)

    database_actioner = DatabaseActioner()
    recordset = database_actioner.recordset("some connection", "test sql")

    assert recordset.headings == test_headings
    assert recordset.data == test_data


def test_record_method(mocker):
    test_headings = ["h1", "h2"]
    test_data = [("a", "b"), ("c", "d")]

    def mocked_get_data(self, connection, sql, params, reference):
        return test_headings, test_data

    class MockedRecord(simqle.actioner.Record):
        def __init__(self, headings, data):
            self.headings = headings
            self.data = data

    mocker.patch.object(simqle.actioner.DatabaseActioner, "get_data", new=mocked_get_data)
    mocker.patch("simqle.actioner.Record", new=MockedRecord)

    database_actioner = DatabaseActioner()
    record = database_actioner.record("some connection", "test sql")

    assert record.headings == test_headings
    assert record.data == test_data


def test_recordscalar_method(mocker):
    test_headings = ["h1", "h2"]
    test_data = [("a", "b"), ("c", "d")]

    def mocked_get_data(self, connection, sql, params, reference):
        return test_headings, test_data

    class MockedRecordScalar(simqle.actioner.RecordScalar):
        def __init__(self, headings, data):
            self.headings = headings
            self.data = data

    mocker.patch.object(simqle.actioner.DatabaseActioner, "get_data", new=mocked_get_data)
    mocker.patch("simqle.actioner.RecordScalar", new=MockedRecordScalar)

    database_actioner = DatabaseActioner()
    record_scalar = database_actioner.record_scalar("some connection", "test sql")

    assert record_scalar.headings == test_headings
    assert record_scalar.data == test_data


def test_get_reference_method():
    actioner = DatabaseActioner()

    # short single line sql
    assert actioner.get_reference(reference=None, sql="short sql") == "short sql"

    # long single line sql
    sql = "long sql long sql long sql long sql long sql long sql long sql"
    assert actioner.get_reference(reference=None, sql=sql) == "long sql long sql lo"

    # short multiline sql
    sql = """
        short
        sql
    """
    assert actioner.get_reference(reference=None, sql=sql) == "short sql"

    # long multiline sql
    sql = """
        long sql line 1
        long sql line 2
        long sql line 3
        long sql line 4
        long sql line 5
    """
    assert actioner.get_reference(reference=None, sql=sql) == "long sql line 1 long"

    # given reference

    assert actioner.get_reference(reference="some reference", sql="some sql") == "some reference"
