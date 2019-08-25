Feature: Connecting to Default Files

  As a SimQLe user
  I want to be able to load a .connections.yaml file from a default location
  so I don't have to specify it in a load_connections method

  @fixture.connections.file
  @fixture.sqlite
  Scenario: load a connections file from a default location
    Given we have a .connections.yaml file in root
    When we load a connection file from a default location
    And we create a table on sqlite
    And we insert an entry on sqlite
    Then the entry exists in the table on sqlite

  @fixture.sqlite
  Scenario: An error occurs when no default files are found
    Given we don't have a .connections.yaml files in default locations
    When we load a connection file from a default location
    Then it throws a NoConnectionsFileError with message "No file_name is specified and no files in default locations are found."
