"""
The SIMQLE_MODE environment variable should determine which set of connections
should be used by the program.

Options are production, development and testing.
"""


def test_mode_changes_connection():
    """Different modes change which connections are used."""
    pass


def test_unknown_mode_throws_error():
    """Unknown modes not in the 3 options throw an error."""
    pass


def test_old_mode_option():
    """
    Older versions of SimQLe looked at SIMQLE_TEST, so this should set
    SIMQLE_MODE to "test".
    """
    pass



