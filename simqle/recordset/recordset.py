"""Define the RecordSet Class."""
from .exceptions import UnknownHeadingError, NoScalarDataError


class RecordSet:
    """
    The RecordSet Object.

    This is the object returned by the ConnectionManager from the recordset
    method. Saves the output of the SQL query once, but allows several ways
    to access it.

    This object is initialised using the normal __init__ method, as there
    isn't much use for an instance of a totally empty recordset. If we need it
    in the future, we can move the __init__ method to a class method.
    """

    def __init__(self, headings, data):
        """
        Initialise this object with data and headings.

        <data> can be None, representing no rows of data for the given
        headings.
        """
        self.data = data or None
        self.headings = headings

    def __bool__(self):
        return self.data is not None

    def __iter__(self):
        if self:
            return iter(self.data)
        return iter(())

    def dict_gen(self):
        """Iterate over records as dictionaries."""
        if self:
            for record in self.data or []:
                yield {h: v for h, v in zip(self.headings, record)}
        return []

    def as_dict(self):
        """
        Return the records as a list of dicts.

        Creates a copy of the data, so isn't very efficient for larger
        data sets.
        """
        if self:
            return [{h: v for h, v in zip(self.headings, record)}
                    for record in self.data or []]
        return []

    def column(self, heading):
        """Return a list of data for a particular heading."""
        try:
            heading_index = self.headings.index(heading)
        except ValueError as e:
            raise UnknownHeadingError(heading) from e

        return [record[heading_index] for record in self.data or []]


class RecordScalar:
    """
    The RecordScalar object assumes that a single value is being returned.

    For example, you would use this when you are trying to find 1 data point
    for a single identity. The same data passed to a RecordSet object is
    passed to this class, however if multiple columns or rows are passed,
    only the top left value is kept.

    Note, we have to distinguish between a NULL value returned, and no rows
    returned. __bool__ is therefore "was a record returned" by the query, and
    then you use self.datum truthiness as per normal.
    """

    def __init__(self, headings, data):
        # Only keep the first heading
        self.heading = headings[0]

        # Only keep None or the first value of data.
        if data:
            self._datum = [data[0][0]]
        else:
            self._datum = None

    def __bool__(self):
        # was a record returned
        return bool(self._datum)

    @property
    def datum(self):
        if not self:
            raise NoScalarDataError()
        return self._datum[0]


class Record:
    """
    The Record object assumes only a single record is being returned.

    If multiple rows are returned, only the first is kept.
    """

    def __init__(self, headings, data):
        self.data = data[0] if data else None

        self.headings = headings
        if self.data:
            self._dict = {k: v for k, v in zip(self.headings, self.data)}
        else:
            self._dict = {}

    def __getitem__(self, heading):
        try:
            return self._dict[heading]
        except KeyError as e:
            raise UnknownHeadingError(heading) from e

    @property
    def as_dict(self):
        return self._dict

    def __bool__(self):
        return self.data is not None
