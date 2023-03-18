"""Test the data containers."""


from pytest import raises
from simqle.container import Record, RecordScalar, RecordSet
from simqle.exceptions import UnknownHeadingError, NoScalarDataError


# -- RecordSet --
def test_record_set_init_with_data():

    test_headings = ["a", "b"]
    test_data = [(1, 2), (3, 4)]

    recordset_with_data = RecordSet(headings=test_headings, data=test_data)

    assert recordset_with_data.headings == test_headings
    assert recordset_with_data.data == test_data

    assert bool(recordset_with_data)

    for idx, row in enumerate(recordset_with_data):
        assert test_data[idx] == row

    recordset_as_dict = recordset_with_data.as_dict()

    assert recordset_as_dict[0] == {"a": 1, "b": 2}
    assert recordset_as_dict[1] == {"a": 3, "b": 4}

    assert recordset_with_data.column("a") == [1, 3]
    assert recordset_with_data.column("b") == [2, 4]

    with raises(UnknownHeadingError):
        recordset_with_data.column("c")


def test_record_set_init_without_data():

    test_headings = ["a", "b"]
    test_data = []

    recordset_without_data = RecordSet(headings=test_headings, data=test_data)

    assert recordset_without_data.headings == test_headings
    assert recordset_without_data.data is None

    assert not bool(recordset_without_data)

    assert list(recordset_without_data) == []

    assert recordset_without_data.as_dict() == []

    assert recordset_without_data.column("a") == []
    assert recordset_without_data.column("b") == []


# -- Record --
def test_record_init():
    test_headings = ["a", "b"]
    test_data = [(1, 2)]
    record = Record(headings=test_headings, data=test_data)

    assert record["a"] == 1
    assert record["b"] == 2

    assert record.as_dict() == {"a": 1, "b": 2}
    assert bool(record)

    with raises(UnknownHeadingError):
        record["not a column"]

    test_headings = ["a", "b"]
    test_data = [(3, 4), (1, 2)]
    record_with_extra_row = Record(headings=test_headings, data=test_data)

    assert record_with_extra_row["a"] == 3
    assert record_with_extra_row["b"] == 4

    assert record_with_extra_row.as_dict() == {"a": 3, "b": 4}
    assert bool(record_with_extra_row)

    empty_record = Record(headings=test_headings, data=[])
    assert not bool(empty_record)



# -- RecordScalar --


def test_record_scalar_init():

    test_headings = ["a"]
    test_data = [(1,)]
    record_scalar = RecordScalar(headings=test_headings, data=test_data)

    assert bool(record_scalar)
    assert record_scalar.heading == "a"
    assert record_scalar.datum == 1
    assert record_scalar.sdatum(default = 2) == 1

    test_headings = ["a"]
    test_data = []
    record_scalar = RecordScalar(headings=test_headings, data=test_data)

    assert not bool(record_scalar)
    assert record_scalar.heading == "a"

    with raises(NoScalarDataError):
        assert record_scalar.datum == 1

    assert record_scalar.sdatum(default = 2) == 2
