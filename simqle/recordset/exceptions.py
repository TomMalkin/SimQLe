"""Define exceptions for the RecordSet Object."""


class UnknownHeadingError(Exception):
    def __init__(self, heading):
        msg = "Unknown heading: [{}]".format(heading)
        super().__init__(msg)
        self.message = msg


class InconsistentRecordSetError(Exception):
    def __init__(self, msg):
        msg = "RecordSet cannot be intialised: {}".format(msg)
        super().__init__(msg)
        self.message = msg


class NotAScalarError(Exception):
    def __init__(self, msg):
        msg = "RecordSet cannot be intialised: {}".format(msg)
        super().__init__(msg)
        self.message = msg


class NoScalarDataError(Exception):
    def __init__(self):
        msg = "No datum was returned"
        super().__init__(msg)
        self.message = msg
