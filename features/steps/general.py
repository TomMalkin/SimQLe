from behave import given, when, then, step
from simqle import (
    ConnectionManager, load_connections, get_engine, get_connection
)
from simqle.exceptions import NoConnectionsFileError, UnknownConnectionError
from constants import CONNECTIONS_FILE, CREATE_TABLE_SYNTAX, TEST_TABLE_NAME
import os
import yaml
from sqlalchemy.engine import Engine
from urllib.parse import quote_plus


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
        "connections": [
                {"name": "my-sqlite-database",
                 "driver": "sqlite:///",
                 "connection": "/tmp/database.db", },
                {"name": "my-sqlite-database-escaped",
                 "driver": "sqlite:///",
                 "connection": "A connection with spaces",
                 "url_escape": True, },
                ]}

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


@when("we execute sql with an error on {con_type}")
def execute_invalid_sql(context, con_type):
    sql = "Invalid syntax"
    con_name = "my-{}-database".format(con_type)

    try:
        context.manager.execute_sql(
            con_name=con_name,
            sql=sql
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


@when("we internally load connections")
def load_internal_connections(context):
    load_connections()

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


@then("it throws a {type}")
def exception_step_no_msg(context, type):
    assert isinstance(context.exc, eval(type)), \
        "Invalid exception - expected " + type


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


@then("the connection has been properly escaped")
def check_escaped_connection(context):
    connection = context.manager.get_engine("my-sqlite-database-escaped")
    url = str(connection.url)
    assert url == "sqlite:///" + quote_plus("A connection with spaces")


@then("the internal connection is loaded")
def internal_connection_is_loaded(context):
    engine = get_engine("my-sqlite-database")
    assert isinstance(engine, Engine)

    engine = get_connection("my-sqlite-database")
    assert isinstance(engine, Engine)

# --- Then ---
