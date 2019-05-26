import subprocess
from behave import fixture

#
#	This is where we could do a personalized machine by machine basis for setup/cleanup
#	just define your fixture and away you go
#


MYSQLCLIENTPATH='/c/Program Files/MySQL/MySQL Server 8.0/bin'
DROP_TABLE_ON_DONE=False

SQLITEPATH='/c/Users/zackb/Downloads/sqlite/sqlite-tools-win32-x86-3280000'
TESTDBFILE='test-databases/sqlite/test.db'
DELETE_DB_FILE_ON_DONE = False

POSTGRESQLPATH='/c/Program Files/PostgreSQL/11/bin'

@fixture
def mysql_fixture(context):
	mysql_setup(context)
	context.add_cleanup(mysql_cleanup)
	return

@fixture
def sqlite_fixture(context):
	sqlite_setup(context)
	context.add_cleanup(sqlite_cleanup)
	return

@fixture
def postgresql_fixture(context):
	postgresql_setup(context)
	context.add_cleanup(postgresql_cleanup)
	return

# kinda insecure but whatever, a test databased
def drop_mysql_test_table():
	subprocess.run([
		'winpty',
		'%s/mysql.exe' % MYSQLCLIENTPATH,
		'--host=localhost',
		'--user=root',
		'--password=ready2go',
		'--execute=DROP TABLE Test',
		'MySQL'
	])

def drop_postgres_table():
	subprocess.run(
		[
			'winpty',
			'%s/psql.exe' % POSTGRESQLPATH,
			'--command=DROP TABLE TEST',
			'postgres'
		],
		env={
			'PGUSER' : 'postgres'
		}
	)

def mysql_setup(context):
	print("Start: Mysql fixture")
	drop_mysql_test_table()

def mysql_cleanup():
	print ("End: Mysql fixture")
	if DROP_TABLE_ON_DONE:
		drop_mysql_test_table()

def sqlite_setup(context):
	print("Start: Sqlite fixture")
	subprocess.run(['rm', TESTDBFILE])
	subprocess.run([
        'winpty',
        '%s/sqlite3.exe' % SQLITEPATH,
        TESTDBFILE, '-A', '-c'
    ]) 

def sqlite_cleanup():
	print ("End: Sqlite fixture")
	if DELETE_DB_FILE_ON_DONE:
		subprocess.run(['rm', TESTDBFILE])

def postgresql_setup(context):
	print("Start: Postgresql fixture")
	drop_postgres_table()

def postgresql_cleanup():
	print("End: Postgresql fixture")
	if DROP_TABLE_ON_DONE:
		drop_postgres_table()