"""General BDD Steps."""

from behave import given, then
from simqle import ConnectionManager
import os
import yaml


# --- Given ---

@given("we have a testmode .connections.yaml file in root")
def add_testmode_connections_file_to_root(context):
    """Set up the context manager with an undefined file."""
    # remove any existing file
    try:
        os.remove("./.connections.yaml")
    except OSError:
        pass

    # define our test file
    connections_file = {
        "connections": [
                {"name": "my-sqlite-database",
                 "driver": "sqlite:///",
                 "connection": "/tmp/production-database.db", },
                ],

        "test-connections": [
                {"name": "my-sqlite-database",
                 "driver": "sqlite:///",
                 "connection": "/tmp/development-database.db", }
                ]
        }

    # write to our test file in a default location
    with open("./.connections.yaml", "w") as outfile:
        yaml.dump(connections_file, outfile)

# --- Given ---


# --- When ---

# --- When ---


# --- Then ---

@then("test mode environment variable changes connection")
def test_mode_environment_check(context):
    """Test that the SIMQLE_TEST env variable switches the connections."""
    # Make sure the project is in production mode
    assert not os.getenv("SIMQLE_TEST", None)

    production_manager = ConnectionManager()
    production_engine = production_manager.get_engine("my-sqlite-database")
    production_url = str(production_engine.url)

    assert production_url == "sqlite:////tmp/production-database.db"

    # Set the test switch to True
    os.environ["SIMQLE_TEST"] = "True"
    development_manager = ConnectionManager()
    development_engine = development_manager.get_engine("my-sqlite-database")
    development_url = str(development_engine.url)

    assert development_url == "sqlite:////tmp/development-database.db"

    # del SIMQLE_TEST for the next test
    del os.environ["SIMQLE_TEST"]

# --- Then ---
