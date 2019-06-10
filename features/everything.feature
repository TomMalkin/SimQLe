Feature: database connections

	As a SimQLe user
	I want to be able to connect to various databases
	So I can execute queries and return recordsets on it

	@fixture.sqlite
	Scenario: sqlite test
		Given we have a sqlite connection
		When we create a table
		AND we insert an entry
		Then the entry exists in the table

	Scenario: mysql test
		Given we have a mysql connection
		When we create a table
		AND we insert an entry
		Then the entry exists in the table

	Scenario: postgresql test
		Given we have a postgresql connection
		When we create a table
		AND we insert an entry
		Then the entry exists in the table
