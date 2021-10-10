"""
The RecordScalar object is used to return a single value from a query.

This allows for convenience such as having only one value in the object, even if
the query returns more than one header or record.

It also allows for identifying 4 levels of data existance easily:

 - query returns data, and that data is "truthy": e.g. "John Citizen"
 - query returns data, and that data is not "truthy": e.g. ""
 - query returns data, and that data is NULL
 - query doesn't return data, e.g. query returns no rows
"""


def test_init():
    """
    When initialised, the RecordScalar object will perform some actions on
    the inputted data.
    """
    pass


def test_bool():
    """
    The truthiness of the RecordScalar object is tricky, because of the 4 levels
    explained above. It was chosen to answer the question: "Was a record returned
    by the query?".
    """
    pass


def test_datum():
    """
    datum() is used to get at the data that was returned. It assumes that at
    least one record is returned, and if it isn't an error is thrown.
    """
    pass


def test_sdatum():
    """
    sdatum() is used to "safely" return a single value, by allowing a default
    parameter which will be returned in the case that no rows were returned
    by the query.
    """
    pass


