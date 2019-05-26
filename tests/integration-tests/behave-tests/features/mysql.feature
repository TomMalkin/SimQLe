Feature: Mysql database connection


@fixture.mysql
Scenario: End to end test
	Given we have a "mysql" connection
	When we create a table
	AND we update an entry
	Then the table exists
	AND the entry exists in the database