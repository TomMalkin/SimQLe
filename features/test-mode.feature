Feature: test mode

	As a SimQLe user
	I want to be able to change SimQLe to be in Test Mode
	So I can write integration tests that look at development databases

	@fixture.connections.file
	@fixture.sqlite
	Scenario: Test Mode
		Given we have a testmode .connections.yaml file in root
		Then test mode environment variable changes connection
