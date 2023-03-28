"""Test the import of all the exceptions."""

def test_import():
    from simqle.exceptions import (
        NoConnectionsFileError,
        UnknownConnectionError,
        EnvironSyncError,
        UnknownSimqleMode,
        UnknownHeadingError,
        NoScalarDataError,
    )
