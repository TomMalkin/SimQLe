"""
SimQLe uses a ConnectionManager class instance to store all the config used
in the project.
"""

def test_connection_manager_init(mocker):
    """Initialising a ConnectionManager object will preload some configs."""
    mocker.patch("ConnectionManager._get_mode")
    cm = ConnectionManager()




# public methods

def test_recordset():
    """recordset() is used to get a RecordSet object."""


def test_record():
    """record() is used to get a Record object."""


def test_recordscalar():
    """recordscalar() is used to get a RecordScalar object."""

def test_execute_sql():
    """
    execute_sql() is used to execute on the database, without expecting a
    return value.
    """

def test_get_engine():
    """
    get_engine is used to get the connection that can be used by other
    libraries
    """

# private methods


def test_private_recordset():
    """
    Each of the return types uses a basic recordset return of data function
    _recordset().
    """
    pass


def test_load_yaml_file():
    """.yaml files are loaded using _load_yaml_file()."""
    pass


def test_get_connection():
    """
    Connection objects are accessed using a con_name, and are returned using
    _get_connection().
    """
    pass


def test_check_default_connections():
    """
    _check_default_connections() is used to check that the default connectiong
    is configured correctly.
    """
    pass


def test_con_name():
    """
    _con_name() is used to return a con_name if just the default is required.
    """


def test_get_mode():
    """
    _get_mode() is used to get the SimQLe mode from the apparent environment variables.
    """
    pass


def test_get_mode_name():
    """
    _get_mode_name() is used to get the name of the mode title used in the
    .connections.yaml file.
    """
    pass

# backwards compatibility

def test_get_connection():
    """get_connection was renamed to get_engine."""
    pass


def test_reset_connections():
    """
    reset_connections is used to reset the ConnectionManager object. There is no
    known use cases for this method, so will remove.
    """
    pass
