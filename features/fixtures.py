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
    except OSError:
        pass
