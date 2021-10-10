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
