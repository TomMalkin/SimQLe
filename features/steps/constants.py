"""Constants for BDD Testing."""

CONN_DIR = "./features/test-connection-files/"
CONNECTIONS_FILE = CONN_DIR + ".connections.yaml"
CONNECTIONS_FILE_WITH_DEFAULT = CONN_DIR + ".connections-with-default.yaml"
CONNECTIONS_FILE_WITH_DEFAULTS = CONN_DIR + ".connections-with-2-defaults.yaml"
CONNECTIONS_FILE_WITH_WRONG_DEFAULTS = CONN_DIR + \
                                       ".connections-with-wrong-defaults.yaml"

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

    "sqlserver":
        """
        create table {} (
            id int primary key identity(1, 1),
            testfield nvarchar(100)
        )
        """.format(TEST_TABLE_NAME),

    "mariadb":
        """
        create table {} (
            id integer primary key auto_increment,
            testfield text
        )
        """.format(TEST_TABLE_NAME),
}
