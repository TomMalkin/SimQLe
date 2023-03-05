"""Test the DatabaseActioner class."""
import pytest
import simqle
from simqle.actioner import DatabaseActioner, Record, RecordScalar, RecordSet, Transaction


def test_execute_sql_method_success(mocker, mocked_timer, mocked_connection, mocked_transaction):

    test_sql = "some sql"
    test_config = {"some": "config"}

    test_connection = mocked_connection(test_config)

    mocker.patch("simqle.actioner.Transaction", new=mocked_transaction)

    execute_mock = mocker.patch.object(Transaction, "execute", autospec=True)
    finalise_mock = mocker.patch.object(Transaction, "finalise", autospec=True)
    commit_mock = mocker.patch.object(Transaction, "commit", autospec=True)
    rollback_mock = mocker.patch.object(Transaction, "rollback", autospec=True)

    mocker.patch.object(DatabaseActioner, "get_reference", return_value="some reference")
    mocker.patch("simqle.actioner.bind_sql", autospec=True, return_value=test_sql)
    mocker.patch("simqle.actioner.Timer", new=mocked_timer(2))

    test_actioner = DatabaseActioner()

    test_actioner.execute_sql(connection=test_connection, sql=test_sql)

    # assert that these transaction methods were called
    execute_mock.assert_called_once_with(mocker.ANY, test_sql)
    commit_mock.assert_called_once()
    finalise_mock.assert_called_once()

    # and the transaction wasn't rolled back
    rollback_mock.assert_not_called()


def test_execute_sql_method_failure(mocker, mocked_timer, mocked_connection, mocked_transaction):

    test_sql = "some sql"
    test_config = {"some": "config"}

    test_connection = mocked_connection(test_config)

    mocker.patch("simqle.actioner.Transaction", new=mocked_transaction)

    execute_mock = mocker.patch.object(
        Transaction,
        "execute",
        autospec=True,
        side_effect=KeyError(),
    )
    finalise_mock = mocker.patch.object(Transaction, "finalise", autospec=True)
    commit_mock = mocker.patch.object(Transaction, "commit", autospec=True)
    rollback_mock = mocker.patch.object(Transaction, "rollback", autospec=True)

    mocker.patch.object(DatabaseActioner, "get_reference", return_value="some reference")
    mocker.patch("simqle.actioner.bind_sql", autospec=True, return_value=test_sql)
    mocker.patch("simqle.actioner.Timer", new=mocked_timer(2))

    test_actioner = DatabaseActioner()

    with pytest.raises(KeyError):
        test_actioner.execute_sql(connection=test_connection, sql=test_sql)

        # the original execute is called and causes an error
        execute_mock.assert_called_once_with(mocker.ANY, test_sql)

        # the transaction shouldn't be committed
        commit_mock.assert_not_called()

        # the rollback should be called to undo the execution
        rollback_mock.assert_called_once()

        # and finalise is always called
        finalise_mock.assert_called_once()


def test_get_data_method_success(mocker, mocked_timer, mocked_connection, mocked_transaction):

    test_sql = "some sql"
    test_config = {"some": "config"}

    test_connection = mocked_connection(test_config)

    mocker.patch("simqle.actioner.Transaction", new=mocked_transaction)

    get_data_mock = mocker.patch.object(Transaction, "get_data", autospec=True, return_value=(1, 2))
    finalise_mock = mocker.patch.object(Transaction, "finalise", autospec=True)
    commit_mock = mocker.patch.object(Transaction, "commit", autospec=True)
    rollback_mock = mocker.patch.object(Transaction, "rollback", autospec=True)

    mocker.patch.object(DatabaseActioner, "get_reference", return_value="some reference")
    mocker.patch("simqle.actioner.bind_sql", autospec=True, return_value=test_sql)
    mocker.patch("simqle.actioner.Timer", new=mocked_timer(2))

    test_actioner = DatabaseActioner()

    test_actioner.get_data(connection=test_connection, sql=test_sql)

    # assert that these transaction methods were called
    get_data_mock.assert_called_once_with(mocker.ANY, test_sql)
    commit_mock.assert_called_once()
    finalise_mock.assert_called_once()

    # and the transaction wasn't rolled back
    rollback_mock.assert_not_called()


def test_get_data_method_failure(
    mocker, mocked_timer, mocked_connection, mocked_transaction, generic_exception
):

    test_sql = "some sql"
    test_config = {"some": "config"}

    test_connection = mocked_connection(test_config)

    mocker.patch("simqle.actioner.Transaction", new=mocked_transaction)

    get_data_mock = mocker.patch.object(
        Transaction, "get_data", autospec=True, side_effect=generic_exception(), return_value=(1, 2)
    )
    finalise_mock = mocker.patch.object(Transaction, "finalise", autospec=True)
    commit_mock = mocker.patch.object(Transaction, "commit", autospec=True)
    rollback_mock = mocker.patch.object(Transaction, "rollback", autospec=True)

    mocker.patch.object(DatabaseActioner, "get_reference", return_value="some reference")
    mocker.patch("simqle.actioner.bind_sql", autospec=True, return_value=test_sql)
    mocker.patch("simqle.actioner.Timer", new=mocked_timer(2))

    test_actioner = DatabaseActioner()

    with pytest.raises(generic_exception):
        test_actioner.get_data(connection=test_connection, sql=test_sql)

        # the original execute is called and causes an error
        get_data_mock.assert_called_once_with(mocker.ANY, test_sql)

        # the transaction shouldn't be committed
        commit_mock.assert_not_called()

        # the rollback should be called to undo the execution
        rollback_mock.assert_called_once()

        # and finalise is always called
        finalise_mock.assert_called_once()


def test_recordset_method(mocker):

    test_headings = ["h1", "h2"]
    test_data = [("a", "b"), ("c", "d")]

    mocker.patch.object(
        simqle.actioner.DatabaseActioner,
        "get_data",
        return_value=(test_headings, test_data),
    )

    class MockedRecordSet(RecordSet):
        def __init__(self, headings, data):
            self.headings = headings
            self.data = data

    mocker.patch("simqle.actioner.RecordSet", new=MockedRecordSet)

    database_actioner = DatabaseActioner()
    recordset = database_actioner.recordset("some connection", "test sql")

    assert recordset.headings == test_headings
    assert recordset.data == test_data


def test_record_method(mocker):

    test_headings = ["h1", "h2"]
    test_data = [("a", "b"), ("c", "d")]

    mocker.patch.object(
        simqle.actioner.DatabaseActioner,
        "get_data",
        return_value=(test_headings, test_data),
    )

    class MockedRecord(Record):
        def __init__(self, headings, data):
            self.headings = headings
            self.data = data

    mocker.patch("simqle.actioner.Record", new=MockedRecord)

    database_actioner = DatabaseActioner()
    record = database_actioner.record("some connection", "test sql")

    assert record.headings == test_headings
    assert record.data == test_data


def test_record_scalar_method(mocker):

    test_headings = ["h1", "h2"]
    test_data = [("a", "b"), ("c", "d")]

    mocker.patch.object(
        simqle.actioner.DatabaseActioner,
        "get_data",
        return_value=(test_headings, test_data),
    )

    class MockedRecordScalar(Record):
        def __init__(self, headings, data):
            self.headings = headings
            self.data = data

    mocker.patch("simqle.actioner.RecordScalar", new=MockedRecordScalar)

    database_actioner = DatabaseActioner()
    record_scalar = database_actioner.record_scalar("some connection", "test sql")

    assert record_scalar.headings == test_headings
    assert record_scalar.data == test_data


# def test_record_method(mocker):
# test_headings = ["h1", "h2"]
# test_data = [("a", "b"), ("c", "d")]

# def mocked_get_data(self, connection, sql, params, reference):
# return test_headings, test_data

# class MockedRecord(simqle.actioner.Record):
# def __init__(self, headings, data):
# self.headings = headings
# self.data = data

# mocker.patch.object(simqle.actioner.DatabaseActioner, "get_data", new=mocked_get_data)
# mocker.patch("simqle.actioner.Record", new=MockedRecord)

# database_actioner = DatabaseActioner()
# record = database_actioner.record("some connection", "test sql")

# assert record.headings == test_headings
# assert record.data == test_data


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
