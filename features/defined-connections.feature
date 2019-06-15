Feature: database connections

	As a SimQLe user
	I want to be able to connect to various databases
	So I can execute queries and return recordsets on it

	@fixture.sqlite
	Scenario: sqlite test
		When we load the test connections file
		AND we create a table on sqlite
		AND we insert an entry on sqlite
		Then the entry exists in the table on sqlite

	Scenario: mysql test
		When we load the test connections file
		AND we create a table on mysql
		AND we insert an entry on mysql
		Then the entry exists in the table on mysql

	Scenario: postgresql test
		When we load the test connections file
		AND we create a table on postgresql
		AND we insert an entry on postgresql
		Then the entry exists in the table on postgresql

	@fixture.sqlite
	Scenario: get engine test
		When we load a sqlite connection from the test connections file
		Then we can get the connection object for sqlite

	@fixture.sqlite
	Scenario: reset connections test
		When we load a sqlite connection from the test connections file
		Then we can reset the connections

	@fixture.sqlite
	Scenario: An error occurs when an unknown connection name is given
		When we load the test connections file
		AND we create a table on wrongname
		Then it throws a UnknownConnectionError with message "Unknown connection my-wrongname-database"
