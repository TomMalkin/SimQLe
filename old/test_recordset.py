"""
The RecordSet class is used to return data that has more than one record of data.
"""


def test_recordset_init():
    """When initialised, the Recordset sets some config."""
    pass


# dunder methods

def test_bool():
    """The truthiness of this object is given as whether data was returned."""
    pass


def test_iter():
    """
    When iterated over, this object will loop over the records in data.
    """
    pass


def test_dict_gen():
    """
    dict_gen() is used to loop over records in the data as a dictionary without
    loading the whole dataset into a dict object, to save on memory.
    """
    pass


def test_as_dict():
    """
    as_dict() is used to get at the data as a dictionary by converting it into
    a dict and returning it.
    """
    pass


def test_column():
    """
    column() is used to return just one column identified by its header as a
    list.
    """
    pass
