"""
SimQLe uses a ConnectionManager class instance to store all the config used
in the project.
"""
from simqle import ConnectionManager
from simqle.connection_manager import _Connection
import simqle

import uuid
from uuid import UUID


def test_connection_manager_init(mocker, get_connection_manager_mock, test_config):
    """Initialising a ConnectionManager object will preload some configs."""
    cm = get_connection_manager_mock()

    assert cm.config == test_config
    assert cm.connections == {}
    assert cm._default_connection_name is None
    assert cm.mode == "production"
    assert cm.mode_name == "connections"


# --- public methods ---


def test_recordset_method(mocker, get_connection_manager_mock):
    """recordset() is used to get a RecordSet object."""
    test_headings = ["header 1", "header 2"]
    test_data = [
        ("row 1 item 1", "row 1 item 2"),
        ("rows2 item 1", "rows2 item 2"),
    ]
    mocker.patch.object(
        ConnectionManager,
        "_recordset",
        new=lambda self, sql, con_name, params, reference: (test_headings, test_data),
    )

    cm = get_connection_manager_mock()

    sql = "sql"
    con_name = "test"

    patched_recordset = mocker.patch("simqle.connection_manager.RecordSet", autospec=True)

    recordset = cm.recordset(sql)

    patched_recordset.assert_called_once_with(headings=test_headings, data=test_data)


def test_record_method(mocker, get_connection_manager_mock):
    """record is used to get a Record object."""
    test_headings = ["header 1", "header 2"]
    test_data = [
        ("row 1 item 1", "row 1 item 2"),
    ]
    mocker.patch.object(
        ConnectionManager,
        "_recordset",
        new=lambda self, sql, con_name, params, reference: (test_headings, test_data),
    )

    cm = get_connection_manager_mock()

    sql = "sql"
    con_name = "test"

    patched_record = mocker.patch("simqle.connection_manager.Record", autospec=True)

    recordset = cm.record(sql)

    patched_record.assert_called_once_with(headings=test_headings, data=test_data)


def test_record_scalar_method(mocker, get_connection_manager_mock):
    """record_scalar() is used to get a RecordScalar object."""
    test_headings = ["header 1"]
    test_data = [
        ("row 1 item 1"),
    ]
    mocker.patch.object(
        ConnectionManager,
        "_recordset",
        new=lambda self, sql, con_name, params, reference: (test_headings, test_data),
    )

    cm = get_connection_manager_mock()

    sql = "sql"
    con_name = "test"

    patched_record_scalar = mocker.patch("simqle.connection_manager.RecordScalar", autospec=True)

    record_scalar = cm.record_scalar(sql)

    patched_record_scalar.assert_called_once_with(headings=test_headings, data=test_data)


def test_execute_sql_method(mocker, get_connection_manager_mock, get_connection_mock):
    """
    execute_sql() is used to execute on the database, without expecting a
    return value.
    """
    cm = get_connection_manager_mock()

    mocker.patch("uuid.uuid4", new=lambda: UUID("e87f2fd8-4dd3-4921-89ad-401b1ccb18d3"))
    mocker.patch.object(
        ConnectionManager,
        "_get_reference",
        new=lambda self, reference: "test reference",
    )
    mocker.patch.object(
        ConnectionManager,
        "_con_name",
        new=lambda self, con_name: "test con_name",
    )
    mocker.patch.object(
        ConnectionManager,
        "_get_connection",
        new=lambda self, con_name: get_connection_mock(),  # shouldn't be a string
    )
    mocker.patch("time.time", new=lambda: 1635058080.7687786)
    mocker.patch.object(_Connection, "execute_sql", auto_spec=True)

    cm.execute_sql(sql="test")

    _Connection.execute_sql.assert_called_once()


def test_get_engine_method(mocker):
    """
    get_engine() is used to return a SQLAlchemy connection that can be used by other libraries.
    """
    pass


# --- private methods ---


def test_recordset_method_private(mocker):
    """
    Each of the return types uses a basic recordset return of data function
    _recordset().
    """
    pass


def test_load_yaml_file_private(mocker):
    """.yaml files are loaded using _load_yaml_file()."""
    pass


def test_get_connection_private(mocker):
    """
    Connection objects are accessed using a con_name, and are returned using
    _get_connection().
    """
    pass


def test_load_default_connection_private(mocker):
    """
    The _load_default_connection() method is used to
    """
    pass


def test_con_name_private(mocker):
    """
    _con_name() is used to return a con_name if just the default is required.
    """
    pass


def test_get_default_connection_private(mocker):
    """
    _check_default_connections() is used to check that the default connectiong
    is configured correctly.
    """
    pass


def test_get_mode_private(mocker):
    """
    _get_mode() is used to get the SimQLe mode from the apparent environment variables.
    """
    pass


def test_get_mode_name_private(mocker):
    """
    _get_mode_name() is used to get the name of the mode title used in the
    .connections.yaml file.
    """
    pass


def test_load_config_private(mocker):
    """
    The _load_config() method is used to
    """
    pass
