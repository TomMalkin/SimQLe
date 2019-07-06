"""General BDD Steps."""

from behave import given, then, when
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

        "dev-connections": [
            {"name": "my-sqlite-database",
             "driver": "sqlite:///",
             "connection": "/tmp/development-database.db", }
        ],

        "test-connections": [
                {"name": "my-sqlite-database",
                 "driver": "sqlite:///",
                 "connection": "/tmp/test-database.db", }
                ]
        }

    # write to our test file in a default location
    with open("./.connections.yaml", "w") as outfile:
        yaml.dump(connections_file, outfile)

# --- Given ---


# --- When ---

@when("we load an unknown connection mode")
def test_mode_environment_check(context):
    try:
        os.environ["SIMQLE_MODE"] = "wrongmode"
        _ = ConnectionManager()
        context.exc = None
    except Exception as e:
        del os.environ["SIMQLE_MODE"]
        context.exc = e

# --- When ---


# --- Then ---

@then("simqle mode environment variable changes connection type")
def test_mode_environment_check(context):
    """Test that the SIMQLE_MODE env variable switches the connections."""
    # When there is no SIMQLE_MODE set, production mode is used by default
    assert os.getenv("SIMQLE_MODE", None) is None

    production_manager = ConnectionManager()
    production_engine = production_manager.get_engine("my-sqlite-database")
    production_url = str(production_engine.url)

    assert production_url == "sqlite:////tmp/production-database.db"


    # when SIMQLE_MODE is "production", then production mode is active
    os.environ["SIMQLE_MODE"] = "production"

    production_manager = ConnectionManager()
    production_engine = production_manager.get_engine("my-sqlite-database")
    production_url = str(production_engine.url)

    assert production_url == "sqlite:////tmp/production-database.db"


    # when SIMQLE_MODE is "development", then development mode is active
    os.environ["SIMQLE_MODE"] = "development"
    development_manager = ConnectionManager()
    development_engine = development_manager.get_engine("my-sqlite-database")
    development_url = str(development_engine.url)

    assert development_url == "sqlite:////tmp/development-database.db"

    # when SIMQLE_MODE is "testing", then testing mode is active
    os.environ["SIMQLE_MODE"] = "testing"
    development_manager = ConnectionManager()
    development_engine = development_manager.get_engine("my-sqlite-database")
    development_url = str(development_engine.url)

    assert development_url == "sqlite:////tmp/test-database.db"


    # del SIMQLE_MODE for the next test
    del os.environ["SIMQLE_MODE"]


@then("simqle test environment variable changes connection type")
def test_mode_environment_check(context):
    """Test that the SIMQLE_TEST env variable switches the connections to test
    mode, despite SIMQLE_MODE."""
    # When there is no SIMQLE_MODE set, production mode is used by default
    assert os.getenv("SIMQLE_TEST", None) is None

    production_manager = ConnectionManager()
    production_engine = production_manager.get_engine("my-sqlite-database")
    production_url = str(production_engine.url)

    assert production_url == "sqlite:////tmp/production-database.db"

    # when SIMQLE_TEST is "true", then test mode is active
    os.environ["SIMQLE_TEST"] = "true"
    test_manager = ConnectionManager()
    test_engine = test_manager.get_engine("my-sqlite-database")
    test_url = str(test_engine.url)

    assert test_url == "sqlite:////tmp/test-database.db"

    # Same thing, despite SIMQLE_MODE
    os.environ["SIMQLE_TEST"] = "true"
    os.environ["SIMQLE_MODE"] = "development"
    test_manager = ConnectionManager()
    test_engine = test_manager.get_engine("my-sqlite-database")
    test_url = str(test_engine.url)

    assert test_url == "sqlite:////tmp/test-database.db"

    del os.environ["SIMQLE_MODE"]
    del os.environ["SIMQLE_TEST"]

# --- Then ---
