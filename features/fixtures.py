from behave import fixture
import os


@fixture
def sqlite_database(context):
    sqlite_cleanup()
    context.add_cleanup(sqlite_cleanup)
    return


def sqlite_cleanup():
    # make sure the database file doesn't exist before running
    tmp_databases = [
        "/tmp/database.db",
        "/tmp/production-database.db",
        "/tmp/development-database.db",
        "/tmp/test-database.db",
        "/tmp/default-database.db",
    ]

    for tmp_database in tmp_databases:
        try:
            os.remove(tmp_database)

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
