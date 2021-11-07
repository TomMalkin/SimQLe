"""Test the config validators."""

from simqle.config_loader import (
    ConfigValidator,
    DefaultConnectionConfigValidator,
    MatchingConnectionNamesValidator,
)


def test_config_validator_init(mocker):
    test_config = {"some config", "some value"}
    # config_validator = ConfigValidator(test_config)
    pass


def test_validate_method(mocker):
    pass


def test_check_default_connections_method(mocker):
    pass


def test_check_connection_names_match_method(mocker):
    pass


def test_default_connection_config_validator_init():
    test_config = {"some config", "some value"}
    test_class = DefaultConnectionConfigValidator(test_config)
    assert test_class.config == test_config


def test_get_default_from_connection_type_method():
    pass


def test_validate_method(mocker):
    pass


def test_matching_connection_names_validator_init():
    test_config = {"some config", "some value"}
    test_class = MatchingConnectionNamesValidator(test_config)
    assert test_class.config == test_config


def test_validate_method(mocker):
    pass
