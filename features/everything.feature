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

Feature: Connecting to Default Files

	As a SimQLe user
	I want to be able to load a .connections.yaml file from a default location
	so I don't have to specify it in a load_connections method

	@fixture.sqlite
	Scenario: no filename test
		Given we have an undefined connection file
		When we create a .connections.yaml file in the root
		AND we create a table
		AND we insert an entry
		Then the entry exists in the table
