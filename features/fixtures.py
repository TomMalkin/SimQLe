from behave import fixture
import os


@fixture
def sqlite_database(context):
    sqlite_cleanup()
    context.add_cleanup(sqlite_cleanup)
    return


def sqlite_cleanup():
    # make sure the database file doesn't exist before running
    try:
        os.remove("/tmp/database.db")
        os.remove("/tmp/production-database.db")
        os.remove("/tmp/development-database.db")
        os.remove("/tmp/default-database.db")

    except OSError:
        pass


@fixture
def connections_file(context):
    context.add_cleanup(connections_file_cleanup)


def connections_file_cleanup():
    try:
        os.remove("./.connections.yaml")
    except OSError:
        pass
