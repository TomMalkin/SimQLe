from behave import given, when, then, step
from simqle import ConnectionManager
from simqle.exceptions import NoConnectionsFileError, UnknownConnectionError
from constants import CONNECTIONS_FILE, CREATE_TABLE_SYNTAX, TEST_TABLE_NAME
import os
import yaml
from sqlalchemy.engine import Engine


# --- Given ---

@given("we have a .connections.yaml file in root")
def add_connections_file_to_root(context):
    """Set up the context manager with an undefined file."""
    # remove any existing file
    try:
        os.remove("./.connections.yaml")
    except OSError:
        pass

    # define our test file
    connections_file = {
        "connections": [{
            "name": "my-sqlite-database",
            "driver": "sqlite:///",
            "connection": "/tmp/database.db",
        }]
    }

    # write to our test file in a default location
    with open("./.connections.yaml", "w") as outfile:
        yaml.dump(connections_file, outfile)


@given("we don't have a .connections.yaml files in default locations")
def remove_default_connections_files(context):
    try:
        os.remove("./.connections.yaml")
    except OSError:
        pass

# --- Given ---


# --- When ---

@when("we load the test connections file")
def load_test_connection_file(context):
    """Set up the context manager for a given connection_type."""
    # context.connection_type = connection_type
    # context.connection_name = "my-{}-database".format(context.connection_type)
    try:
        context.manager = ConnectionManager(file_name=CONNECTIONS_FILE)
        context.exc = None
    except Exception as e:
        context.exc = e


@when("we load a connection file from a default location")
def load_default_connection_file(context):
    """Set up the context manager for a given connection_type."""
    try:
        # context.connection_type = "sqlite"
        # context.connection_name = "my-sqlite-database"
        context.manager = ConnectionManager()
        context.exc = None
    except Exception as e:
        context.exc = e


@when("we create a table on {con_type}")
def create_a_table(context, con_type):
    # create_table_sql = CREATE_TABLE_SYNTAX[context.connection_type]
    create_table_sql = CREATE_TABLE_SYNTAX.get(con_type)
    con_name = "my-{}-database".format(con_type)

    try:
        context.manager.execute_sql(
            con_name=con_name,
            sql=create_table_sql
        )
        context.exc = None
    except Exception as e:
        context.exc = e


@when("we insert an entry on {con_type}")
def update_an_entry(context, con_type):
    insert_record_sql = """
        INSERT INTO {} (testfield)
        VALUES ('foo')
        """.format(TEST_TABLE_NAME)

    con_name = "my-{}-database".format(con_type)

    context.manager.execute_sql(con_name=con_name,
                                sql=insert_record_sql)

# --- When ---


# --- Then ---

@then("the entry exists in the table on {con_type}")
def entry_exists(context, con_type):
    sql = "SELECT id, testfield FROM {}".format(TEST_TABLE_NAME)
    # SHOULD : probably catch exact right type of exception
    con_name = "my-{}-database".format(con_type)
    rst = context.manager.recordset(
        con_name=con_name,
        sql=sql
    )

    # print("for connection {}".format(context.connection_type))
    #
    # print("rst returned:")
    # print(rst)

    correct_rst = (
        # data
        [(1, "foo")],

        # headings
        ["id", "testfield"]
    )

    # print("the correct rst is:")
    # print(correct_rst)

    assert rst == correct_rst


@then('it throws a {type} with message "{msg}"')
def exception_step(context, type, msg):
    assert isinstance(context.exc, eval(type)), \
        "Invalid exception - expected " + type

    assert context.exc.message == msg, "Invalid message - expected " + msg


@then("we can get the connection object for {connection}")
def get_connection_object(context, connection):
    con_name = "my-{}-database".format(connection)

    engine = context.manager.get_engine(con_name)
    assert isinstance(engine, Engine)

    engine = context.manager.get_connection(con_name)
    assert isinstance(engine, Engine)


@then("we can reset the connections")
def reset_connections(context):
    context.manager.get_engine("my-sqlite-database")
    assert context.manager.connections != {}
    context.manager.reset_connections()
    assert context.manager.connections == {}

# --- Then ---
