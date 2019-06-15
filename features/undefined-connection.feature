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
