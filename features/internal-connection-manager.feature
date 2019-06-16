Feature: database connections

	As a SimQLe user
	I want to be able to use the internal connection manager
	So each module can utilise the same connections

	@fixture.connections.file
	@fixture.sqlite
	Scenario: Internal Manager test
		Given we have a .connections.yaml file in root
		When we internally load connections
		Then the internal connection is loaded
