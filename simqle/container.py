"""
Define the data containers that represent the data that is returned from the database.

The three types of data that are commonly returned are:
 - recordsets - one or more fields with one or more rows
 - records - one of more fields but only one row
 - recordscalar - one field with one row, aka one point of data


DataContainer is the common set of setup that all the data containers undergo before filtering to
their type of return data.
"""
from .exceptions import NoScalarDataError, UnknownHeadingError
from .logging import logger


class RecordSet:
    """Represents a data container with 1+ fields and 1+ rows."""

    def __init__(self, headings, data):
        self.headings = headings
        self.data = data or None

    def __bool__(self):
        """Return if this recordset has data."""
        return self.data is not None

    def __iter__(self):
        """Iterate through the data records."""
        if self.data:
            return iter(self.data)
        return iter(())

    def dict_gen(self):
        """Iterate over records as dictionaries."""
        if self.data:
            for record in self.data:
                yield dict(zip(self.headings, record))

    def as_dict(self):
        """
        Return the records as a list of dicts.

        Creates a copy of the data, so isn't very efficient for larger
        data sets.
        """
        if self.data:
            return [dict(zip(self.headings, self.data)) for record in self.data or []]
        return []

    def column(self, heading):
        """Return a list of data for a particular heading."""
        try:
            heading_index = self.headings.index(heading)
        except ValueError as exception:
            raise UnknownHeadingError(heading) from exception

        return [record[heading_index] for record in self.data or []]


class Record:
    """
    Represents a data container with 1+ fields but only a single row.

    If multiple rows are returned, only the first is kept.
    """

    def __init__(self, headings, data):
        if len(data) > 1:
            logger.warning("Record object initialised with a query that returned more than 1 row.")

        self.headings = headings
        self.data = data[0] if data else None

        self._dict = {}
        if self.data:
            self._dict = dict(zip(self.headings, self.data))

    def __getitem__(self, heading):
        """Return a value based on a heading."""
        try:
            return self._dict[heading]
        except KeyError as exception:
            raise UnknownHeadingError(heading) from exception

    def as_dict(self):
        """Return this record as a dict."""
        return self._dict

    def __bool__(self):
        """Return if this record has data."""
        return self.data is not None


class RecordScalar:
    """
    Represents a data container with 1 field and only a single row.

    In other words, a single value returned from the database. If multiple headings or rows
    are returned, then only the first heading and first row are kept.

    Truthiness for a scalar is slightly more complicated than RecordSet and Record objects, as
    there are 4 possiblities when attempting to get a scalar datum from a database:
     - No data returned
     - The data point was Null (None)
     - The data returned equates to False: like 0 or an empty string
     - the data returned equates to True: like 1 or a non-empty string

    The truthiness is set to the answer to the question: 'Was any value, even null, returned from
    the database?'.
    """

    def __init__(self, headings, data):
        # Only keep the first heading
        self.heading = headings[0]

        # Only keep None or the first value of data.
        if data:
            self.is_data_returned = True
            self._datum = data[0][0]
        else:
            self.is_data_returned = False
            self._datum = None

    def __bool__(self):
        """Was a value, even null, returned from the database?."""
        return self.is_data_returned

    @property
    def datum(self):
        """Return a naive scalar value that assumes it's own existance."""
        if not self.is_data_returned:
            raise NoScalarDataError()
        return self._datum

    def sdatum(self, default=None):
        """
        Return the datum with a default value if the record doesn't exist.

        sdatum stands for Safe Datum, providing a default value instead of
        raising an error if the record doesn't exist.
        """
        if not self:
            return default
        return self._datum
