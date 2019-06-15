Feature: database connections

	As a SimQLe user
	I want to be able to connect to various databases
	So I can execute queries and return recordsets on it

	@fixture.sqlite
	Scenario: sqlite test
		When we load a sqlite connection from the test connections file
		AND we create a table
		AND we insert an entry
		Then the entry exists in the table

	Scenario: mysql test
		When we load a mysql connection from the test connections file
		AND we create a table
		AND we insert an entry
		Then the entry exists in the table

	Scenario: postgresql test
		When we load a postgresql connection from the test connections file
		AND we create a table
		AND we insert an entry
		Then the entry exists in the table
