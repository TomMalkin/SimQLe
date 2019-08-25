Feature: database connections

  As a SimQLe user
  I want to be able to connect to various databases
  So I can execute queries And return recordsets on it

# --- A basic test of each of the supported databases ---

  @fixture.sqlite
  Scenario: sqlite test
    When we load the test connections file
    And we create a table on sqlite
    And we insert an entry on sqlite
    Then the entry exists in the table on sqlite

  Scenario: mysql test
    When we load the test connections file
    And we create a table on mysql
    And we insert an entry on mysql
    Then the entry exists in the table on mysql

  Scenario: postgresql test
    When we load the test connections file
    And we create a table on postgresql
    And we insert an entry on postgresql
    Then the entry exists in the table on postgresql


# --- Test the other return types on sqlite
  @fixture.sqlite
  Scenario: Data exists test
    When we load the test connections file
    And we create a table on sqlite
    And we insert an entry on sqlite
    Then we can return a Recordset
    And we can return a Record
    And we can return a RecordScalar

  @fixture.sqlite
  Scenario: Data doesn't exists test
    When we load the test connections file
    And we create a table on sqlite
    Then we can return an empty Recordset
    And we can return an empty Record
    And we can return an empty RecordScalar


# --- Testing other functionality ---

  @fixture.sqlite
  Scenario: get engine test
    When we load the test connections file
    Then we can get the connection object for sqlite

  @fixture.sqlite
  Scenario: reset connections test
    When we load the test connections file
    Then we can reset the connections

  @fixture.connections.file
  @fixture.sqlite
  Scenario: A connection with url-escape is suitable
    Given we have a .connections.yaml file in root
    When we load a connection file from a default location
    Then the connection has been properly escaped


# --- Error Handling ---

  @fixture.sqlite
  Scenario: An error occurs when an unknown connection name is given
    When we load the test connections file
    And we create a table on wrongname
    Then it throws a UnknownConnectionError with message "Unknown connection my-wrongname-database"

  @fixture.sqlite
  Scenario: A SQL error raises an exception
    When we load the test connections file
    And we execute sql with an error on sqlite
    Then it throws a Exception


# --- Testing default connection functionality ---

  @fixture.sqlite
  Scenario: No connection name loads a default connection
    When we load the test connections file with a default connection
    And we create a table with no connection name
    And we insert an entry with no connection name
    Then the entry exists in the default table

  @fixture.sqlite
  Scenario: Multiple default connections throws an error
    When we load the test connections file with a 2 default connections
    Then it throws a MultipleDefaultConnectionsError with message "More than 1 default connection was specified."

  @fixture.sqlite
  Scenario: No connection name given but no default connection throws an error
    When we load the test connections file
    And we create a table with no connection name
    Then it throws a NoDefaultConnectionError with message "No Connection name was specified but no default connection exists."

  @fixture.sqlite
  Scenario: If the test default connection doesn't match the production default connection it throws an error
    When we load the test connections file with wrong default connections
    Then it throws a EnvironSyncError with message "The default connection in connections doesn't match the default connection in the test connections."
