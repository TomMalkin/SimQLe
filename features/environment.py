
from behave import use_fixture
from fixtures import sqlite_database, connections_file
import time


def before_all(context):
    print("Starting behave tests")
    time.sleep(30)


def before_tag(context, tag):
    if tag == "fixture.sqlite":
        use_fixture(sqlite_database, context)
    elif tag == "fixture.connections.file":
        use_fixture(connections_file, context)


def after_all(context):
    print("Behave tests complete")
