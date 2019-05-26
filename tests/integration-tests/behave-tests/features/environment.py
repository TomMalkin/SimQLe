
import subprocess

from behave import use_fixture
from fixtures import mysql_fixture, sqlite_fixture, postgresql_fixture


def before_all(context):
    print("Starting up")

def before_tag(context, tag):
    if tag == 'fixture.mysql':
        use_fixture(mysql_fixture, context)
    elif tag == 'fixture.sqlite':
        use_fixture(sqlite_fixture, context)
    elif tag == 'fixture.postgresql':
    	use_fixture(postgresql_fixture, context)
    else:
        pass

def after_all(context):
    print("Shutting down")