
from behave import use_fixture
from fixtures import sqlite_database


def before_all(context):
    print("Starting behave tests")


def before_tag(context, tag):
    if tag == 'fixture.sqlite':
        use_fixture(sqlite_database, context)


def after_all(context):
    print("Behave tests complete")
