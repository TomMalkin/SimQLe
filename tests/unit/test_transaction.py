import simqle
from pytest_mock import mocker
from simqle.actioner import Transaction


class MockedEngine:
    def connect(self):
        pass


class MockedConnection(simqle.connection.Connection):
    def __init__(self, config={"some": "config"}):
        self.config = config
        self.name = "test name"
        self.driver = "test driver"
        self.engine = MockedEngine()


class MockedConnectedEngine:
    def begin(self):
        pass

    def close(self):
        pass

    def execute(self, bound_sql):
        pass


class MockedCommunication:
    def commit(self):
        pass

    def rollback(self):
        pass


class MockedTransaction(simqle.actioner.Transaction):
    def __init__(self):
        self.connection = MockedConnection()
        self.engine = MockedEngine()
        self.connected_engine = MockedConnectedEngine()
        self.communication = MockedCommunication()


def test_transaction_init(mocker, mocked_connection):

    mock_engine = mocker.patch.object(simqle.actioner.Transaction, "get_engine")
    mock_connected_engine = mocker.patch.object(simqle.actioner.Transaction, "connect_engine")
    mock_transaction = mocker.patch.object(simqle.actioner.Transaction, "begin_transaction")

    # connection = mocked_connection
    Transaction(connection=mocked_connection)

    mock_engine.assert_called_once()
    mock_connected_engine.assert_called_once()
    mock_transaction.assert_called_once()


def test_transaction_get_engine(mocker):

    test_transaction = MockedTransaction()

    assert test_transaction.get_engine() == test_transaction.connection.engine


def test_transaction_connect_engine(mocker):

    mock_connect = mocker.patch.object(MockedEngine, "connect")

    test_transaction = MockedTransaction()

    test_transaction.connect_engine()
    mock_connect.assert_called_once()


def test_transaction_begin_transaction(mocker):

    mock_communication = mocker.patch.object(MockedConnectedEngine, "begin")

    test_transaction = MockedTransaction()

    test_transaction.begin_transaction()

    mock_communication.assert_called_once()


def test_transaction_rollback(mocker):

    mock_communication_rollback = mocker.patch.object(MockedCommunication, "rollback")

    test_transaction = MockedTransaction()

    test_transaction.rollback()

    mock_communication_rollback.assert_called_once()


def test_transaction_finalise(mocker):

    mock_communication_finalise = mocker.patch.object(MockedConnectedEngine, "close")

    test_transaction = MockedTransaction()

    test_transaction.finalise()

    mock_communication_finalise.assert_called_once()


def test_transaction_execute(mocker):

    test_sql = "some sql"

    mock_communication_execute = mocker.patch.object(MockedConnectedEngine, "execute")

    test_transaction = MockedTransaction()

    test_transaction.execute(bound_sql=test_sql)

    mock_communication_execute.assert_called_once_with(test_sql)


def test_transaction_commit(mocker):

    mock_communication_commit = mocker.patch.object(MockedCommunication, "commit")

    test_transaction = MockedTransaction()

    test_transaction.commit()

    mock_communication_commit.assert_called_once()


def test_transaction_get_data(mocker):

    test_sql = "some sql"

    class MockedResult:
        def fetchall(self):
            return "data"

        def keys(self):
            return ["some", "keys"]

    mocked_execute = mocker.patch.object(
        MockedConnectedEngine, "execute", return_value=MockedResult()
    )

    test_transaction = MockedTransaction()

    headings, data = test_transaction.get_data(test_sql)

    assert headings == ["some", "keys"]
    assert data == "data"

    mocked_execute.assert_called_once_with(test_sql)
