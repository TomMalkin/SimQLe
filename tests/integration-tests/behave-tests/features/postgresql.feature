Feature: Postgresql database connection


@fixture.postgresql
Scenario: End to end test
	Given we have a "postgresql" connection
	When we create a table
	AND we update an entry
	Then the table exists
	AND the entry exists in the database