"""Constants for BDD Testing."""

CONNECTIONS_FILE = "./features/.connections.yaml"

# Create table queries. Each database has it's own SQL syntax for
# creating tables so these are used below.

TEST_TABLE_NAME = "testtable"

CREATE_TABLE_SYNTAX = {

    "sqlite":
        """
        create table {} (
            id integer primary key autoincrement,
            testfield text
        )
        """.format(TEST_TABLE_NAME),

    "mysql":
        """
        create table {} (
            id integer primary key auto_increment,
            testfield text
        )
        """.format(TEST_TABLE_NAME),

    "postgresql":
        """
        create table {} (
            id serial,
            testfield text
        )
        """.format(TEST_TABLE_NAME),

}
