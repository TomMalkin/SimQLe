from behave import *
from simqle.connection_manager import ConnectionManager

## TODO : make this less relative to the current directory
CONFIG_FILE='.connections.yaml'

@given('we have a "{connection_type}" connection')
def create_a_connection(context, connection_type):
	if connection_type not in ['mysql', 'sqlite', 'postgresql']:
		raise Exception('unrecognized connection_type %s' % connection_type)
	else:
		context.connection_type = connection_type
	context.manager = ConnectionManager(file_name=CONFIG_FILE)

@when('we create a table')
def create_a_table(context):
	query = "CREATE TABLE Test (TestColumn1 int, TestColumn2 varchar(30));"
	context.manager.execute_sql(
		'my-%s-database' % context.connection_type, query
	)

@when('we update an entry')
def update_an_entry(context):
	query = "INSERT INTO Test (TestColumn1, TestColumn2) VALUES (1, 'foo')"
	context.manager.execute_sql(
		'my-%s-database' % context.connection_type, query
	)

@then('the table exists')
def table_exists(context):
    query = "SELECT * FROM Test"
    # SHOULD : probably catch exact right type of exception
    try:
        context.manager.execute_sql(
        	'my-%s-database' % context.connection_type, query
        )
        assert (True)
    except:
        assert (False)

@then('the entry exists in the database')
def entry_exists(context):
	query = "SELECT * FROM Test"
	results = context.manager.recordset(
		'my-%s-database' % context.connection_type, query
	)
	assert (results is not None)
