"""Test the Connection class."""

from simqle.connection import Connection


def test_connection_init(mocker, example_configuration):
    config = example_configuration["dev-connections"][0]
    connection = Connection(config=config)


def test_quote_plus(mocker):
    test_config = {
        "name": "test connection",
        "driver": "test driver",
        "connection": "test connection",
        "url_escape": True,
    }

    mocked_create_engine = mocker.patch("simqle.connection.create_engine", return_value="created engine")
    mocked_quote_plus = mocker.patch("simqle.connection.quote_plus", return_value="quote plus string")
    connection = Connection(config=test_config)

    mocked_create_engine.assert_called_once_with("test driverquote plus string")
    mocked_quote_plus.assert_called_once_with("test connection")

    assert connection.engine == "created engine"


