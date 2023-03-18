"""
The Record object is used to get at a single record of data. If extra are
returned by the query to the database, then these are discarded.

This object allows for getting at the data easily with named headers, and
for easily converting to dicts.
"""


def test_init():
    """
    When initialised, the Record object will set some config values.
    """
    pass


def test_get_item():
    """
    The data in this object can be access by passing a header name in a
    normal python get.
    """
    pass


def test_as_dict():
    """
    Get the data in this object as a normal dict of {header: value, ...}
    """
    pass


def test_bool():
    """
    The truthiness of this object is whether one (or more) rows were returned
    by the query to the database.
    """
    pass

# def test_record_basic(mocker, get_connection_manager_mock, caplog):
    # """
    # record() is used to get a Record object.

    # The object can be initialised with a query that returns 1 record.
    # """
    # test_headings = ["header 1", "header 2"]
    # test_data = [("row 1 item 1", "row 1 item 2")]
    # mocker.patch.object(
        # ConnectionManager,
        # "_recordset",
        # new=lambda self, sql, con_name, params: (test_headings, test_data),
    # )

    # cm = get_connection_manager_mock()
    # record = cm.record("test")

    # assert isinstance(record, Record)

    # assert record.data ==  test_data[0]
    # assert record.headings == test_headings

    # assert record._dict == {"header 1": "row 1 item 1","header 2": "row 1 item 2"}

    # assert "Record object initialised with a query that returned more than 1 row." not in caplog.text


# def test_record_multi(mocker, get_connection_manager_mock, caplog):
    # """Record can also be initalised """

    # test_headings = ["header 1", "header 2"]

    # # record initialised with 2+ query length will load first record with a warning
    # test_data_multi = [
        # ("a", "b"),
        # ("c", "d"),
    # ]

    # mocker.patch.object(
        # ConnectionManager,
        # "_recordset",
        # new=lambda self, sql, con_name, params: (test_headings, test_data_multi),
    # )
    # record = cm.record("test")

    # assert record.data ==  ("a", "b")
    # assert record.headings == test_headings
    # assert record._dict == {"header 1": "a", "header 2": "b"}
    # assert "Record object initialised with a query that returned more than 1 row." in  caplog.text

    # # record 

    # # if self.data:
    # # self._dict = {k: v for k, v in zip(self.headings, self.data)}
    # # else:
    # # self._dict = {}
