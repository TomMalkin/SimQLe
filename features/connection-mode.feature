Feature: connection mode changing

	As a SimQLe user
	I want to be able to change SimQLe to be in various modes
	So I can write integration tests that look at test databases

	@fixture.connections.file
	@fixture.sqlite
	Scenario: Changing Connection Mode
		Given we have a testmode .connections.yaml file in root
		Then simqle mode environment variable changes connection type


	# for backwards compatibility, SIMQLE_TEST should autoamatically set SimQLe to test mode
	@fixture.connections.file
	@fixture.sqlite
	Scenario: Test Mode
		Given we have a testmode .connections.yaml file in root
		Then simqle test environment variable changes connection type
