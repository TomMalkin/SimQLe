Feature: Sqlite database connection

	As a SimQLe user
	I want to be able to connect to sqlite as a database
	So I can execute queries and return recordsets on it

	@fixture.sqlite
	Scenario: End to end test
		Given we have a sqlite connection
		When we create a table
		AND we insert an entry
		Then the entry exists in the table
