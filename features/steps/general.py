from behave import given, when, then, step
from simqle import ConnectionManager
from constants import CONNECTIONS_FILE, CREATE_TABLE_SYNTAX, TEST_TABLE_NAME


@given('we have a {connection_type} connection')
def step_impl(context, connection_type):
    context.connection_type = connection_type
    context.connection_name = "my-{}-database".format(context.connection_type)
    context.manager = ConnectionManager(file_name=CONNECTIONS_FILE)


@when('we create a table')
def create_a_table(context):
    create_table_sql = CREATE_TABLE_SYNTAX[context.connection_type]

    context.manager.execute_sql(
        con_name=context.connection_name,
        sql=create_table_sql
    )


@when('we insert an entry')
def update_an_entry(context):
    insert_record_sql = """
        INSERT INTO {} (TestField)
        VALUES ('foo')
        """.format(TEST_TABLE_NAME)

    context.manager.execute_sql(con_name=context.connection_name,
                                sql=insert_record_sql)


@then('the entry exists in the table')
def entry_exists(context):
    sql = "SELECT id, TestField FROM {}".format(TEST_TABLE_NAME)
    # SHOULD : probably catch exact right type of exception
    rst = context.manager.recordset(
        con_name=context.connection_name,
        sql=sql
    )

    print(rst)

    correct_rst = (
        # data
        [(1, "foo")],

        # headings
        ["id", "TestField"]
    )

    print(correct_rst)

    assert rst == correct_rst
