"""Steps testing the multiple possible return types."""

from behave import given, when, then

from features.steps.constants import TEST_TABLE_NAME
from simqle.recordset import RecordSet, RecordScalar, Record
from simqle.recordset.exceptions import UnknownHeadingError, NoScalarDataError


@then("we can return a Recordset")
def recordset_method(context):
    """Test the various Recordset methods"""
    sql = "SELECT id, testfield FROM {}".format(TEST_TABLE_NAME)
    rst = context.manager.recordset(con_name="my-sqlite-database", sql=sql)

    correct_data = [(1, "foo"), (2, "1")]
    correct_dicts = [
        {"id": 1, "testfield": "foo"},
        {"id": 2, "testfield": "1"},
    ]

    assert isinstance(rst, RecordSet)

    assert rst.headings == ["id", "testfield"]
    assert rst.data == correct_data

    # data exists means this is true
    assert bool(rst)

    # standard iteration
    for row, test_row in zip(rst, correct_data):
        assert row == test_row

    # iterate over dicts
    for rst_dict, test_dict in zip(rst.dict_gen(), correct_dicts):
        assert rst_dict == test_dict

    # convert the whole rst into a list of dicts
    for rst_dict, test_dict in zip(rst.as_dict(), correct_dicts):
        assert rst_dict == test_dict

    # iterate over one column
    for value, test_value in zip(rst.column("testfield"), ["foo", "1"]):
        assert value == test_value

    # column with wrong column name raises the correct error
    try:
        _ = rst.column("Not a Column")
        raise
    except UnknownHeadingError:
        pass


@then("we can return a Record")
def record_method(context):
    """Test the various Records methods"""
    sql = "SELECT id, testfield FROM {}".format(TEST_TABLE_NAME)
    record = context.manager.record(con_name="my-sqlite-database", sql=sql)

    assert isinstance(record, Record)

    assert record.headings == ["id", "testfield"]

    # Record.data is just a tuple
    correct_data = (1, "foo")
    assert record.data == correct_data

    # Record.as_dict is a dict, not a list of dicts like RecordSet
    assert record.as_dict == {"id": 1, "testfield": "foo"}

    # the record exists, so returning True
    assert bool(record)

    assert record["id"] == 1
    assert record["testfield"] == "foo"

    try:
        _ = record["wrong field"]
        raise
    except UnknownHeadingError:
        pass


@then("we can return a RecordScalar")
def record_scalar_method(context):
    sql = "SELECT testfield FROM {}".format(TEST_TABLE_NAME)
    scalar = context.manager.record_scalar(con_name="my-sqlite-database",
                                           sql=sql)

    assert isinstance(scalar, RecordScalar)
    assert bool(scalar)

    assert scalar.datum == "foo"

    assert scalar.sdatum("bar") == "foo"


@then("we can return an empty Recordset")
def empty_recordset_method(context):
    """Test the various Recordset methods"""
    sql = "SELECT id, testfield FROM {}".format(TEST_TABLE_NAME)
    rst = context.manager.recordset(con_name="my-sqlite-database", sql=sql)

    assert isinstance(rst, RecordSet)

    assert rst.headings == ["id", "testfield"]
    assert rst.data is None

    # data doesn't exist meaning this is False
    assert not bool(rst)

    # standard iteration
    for _ in rst:
        raise

    # iterate over dicts
    for _ in rst.dict_gen():
        raise

    # convert the whole rst into a list of dicts
    for _ in rst.as_dict():
        raise

    # iterate over one column
    for _ in rst.column("testfield"):
        raise

    # column with wrong column name raises the correct error
    try:
        _ = rst.column("Not a Column")
        raise
    except UnknownHeadingError:
        pass


@then("we can return an empty Record")
def empty_record_method(context):
    """Test the various Records methods"""
    sql = "SELECT id, testfield FROM {}".format(TEST_TABLE_NAME)
    record = context.manager.record(con_name="my-sqlite-database", sql=sql)

    assert isinstance(record, Record)

    assert record.headings == ["id", "testfield"]

    # Record.data is just a tuple
    assert record.data is None

    # Record.as_dict is a dict, not a list of dicts like RecordSet
    assert record.as_dict == {}

    # the record doesn't exist, so returning False
    assert not bool(record)

    try:
        _ = record["testfield"]
        raise
    except UnknownHeadingError:
        pass


@then("we can return an empty RecordScalar")
def empty_record_scalar_method(context):
    sql = "SELECT testfield FROM {}".format(TEST_TABLE_NAME)
    scalar = context.manager.record_scalar(con_name="my-sqlite-database",
                                           sql=sql)

    assert isinstance(scalar, RecordScalar)
    assert not bool(scalar)

    try:
        assert scalar.datum == "foo"
    except NoScalarDataError:
        pass

    assert scalar.sdatum("bar") == "bar"
    assert scalar.sdatum() is None

