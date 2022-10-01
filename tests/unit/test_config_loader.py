"""Test the ConfigLoader and Validator classes."""
import pytest
import simqle
from simqle.config_loader import ConfigLoader, ConfigValidator, DefaultLoader

# --- Config Loader ---


def test_config_loader_init(mocker):
    test_config = {"dev-connections": {"some": "config"}}
    mocker.patch.object(ConfigLoader, "load_config", lambda self: test_config)

    class MockValidator(simqle.config_loader.ConfigValidator):
        def __init__(self, config):
            self.config = config
            self.default_connection_name = "default name"

    mocker.patch("simqle.config_loader.ConfigValidator", new=MockValidator)
    mocker.patch.object(MockValidator, "validate", autospec=True)

    test_config_loader = ConfigLoader("test filename", "development")

    assert test_config_loader.full_config == test_config
    # assert test_config_loader.default_connection_name == "default name"
    assert test_config_loader.config == {"some": "config"}

    test_config_loader.validator.validate.assert_called_once()


def test_load_config_method(mocker):
    class MockedConfigLoader(simqle.config_loader.ConfigLoader):
        def __init__(self, filename, mode):
            self.filename = filename
            self.mode = mode

    # filename isn't given, so config should be loaded from a default location

    test_base_config = {"dev-connections": {"some": "default config"}}

    mocker.patch.object(
        MockedConfigLoader, "load_from_default_location", new=lambda self: test_base_config
    )

    test_config_loader = MockedConfigLoader(None, "development")

    base_config = test_config_loader.load_config()
    assert base_config == test_base_config

    # filename is a dict, so should be loaded straight into config
    test_dict_base_config = {"dev-connections": {"some": "dict config"}}
    test_config_loader = MockedConfigLoader(test_dict_base_config, "development")
    base_config = test_config_loader.load_config()
    assert base_config == test_dict_base_config

    # filename is a filename of a file that exists, so should be loaded from that file
    test_filename_base_config = {"dev-connections": {"some": "filename config"}}
    test_config_loader = MockedConfigLoader("some filename", "development")

    mocker.patch.object(
        MockedConfigLoader, "load_file", new=lambda self, filename: test_filename_base_config
    )

    base_config = test_config_loader.load_config()
    assert base_config == test_filename_base_config

    # filename is a filename of a file that doesn't exist, so FileNotFoundError should be raised

    def mocked_error_load_file(self, filename):
        raise FileNotFoundError()

    mocker.patch.object(MockedConfigLoader, "load_file", new=mocked_error_load_file)

    test_config_loader = MockedConfigLoader("some failed filename", "development")

    with pytest.raises(FileNotFoundError) as exc_info:
        test_config_loader.load_config()

    assert "some failed filename" in str(exc_info.value)


def test_load_from_default_location_method(mocker):
    class MockedConfigLoader(simqle.config_loader.ConfigLoader):
        def __init__(self, filename, mode):
            self.filename = filename
            self.mode = mode

    mock_default_locations = ["location 1", "location 2"]

    test_base_config = {"dev-connections": {"some": "default config"}}

    # file found in first default location
    mocker.patch("simqle.config_loader.DEFAULT_FILE_LOCATIONS", new=mock_default_locations)

    mocker.patch.object(
        MockedConfigLoader, "load_file", new=lambda self, filename: test_base_config
    )

    config_loader = MockedConfigLoader(None, "development")

    result_config = config_loader.load_from_default_location()
    assert result_config == test_base_config

    # file found in second default location
    test_location_2_base_config = {"dev-connections": {"some": "location 2 default config"}}

    def second_location_load_file(self, filename):
        if filename == "location 1":
            raise FileNotFoundError()
        return test_location_2_base_config

    mocker.patch.object(MockedConfigLoader, "load_file", new=second_location_load_file)

    result_config = config_loader.load_from_default_location()
    assert result_config == test_location_2_base_config

    # file not found anywhere raises NoConnectionsFileError
    def error_load_file(self, filename):
        raise FileNotFoundError()

    mocker.patch.object(MockedConfigLoader, "load_file", new=error_load_file)

    with pytest.raises(simqle.exceptions.NoConnectionsFileError) as exc_info:
        result_config = config_loader.load_from_default_location()

    assert "No filename" in str(exc_info.value)


def test_load_file_method(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="test read data"))

    class MockedConfigLoader(simqle.config_loader.ConfigLoader):
        def __init__(self, filename, mode):
            self.filename = filename
            self.mode = mode

    mocker.patch("simqle.config_loader.safe_load", new=lambda text: {"some": "dict"})

    config_loader = MockedConfigLoader("some filename", "development")

    assert config_loader.load_file("something") == {"some": "dict"}


# --- Config Validator ---


def test_config_validator_init():

    config_validator = ConfigValidator({"some": "config"})


def test_validate_method(mocker):

    mocker.patch.object(
        simqle.config_loader.ConfigValidator, "check_default_connections", autospec=True
    )
    mocker.patch.object(
        simqle.config_loader.ConfigValidator, "check_connection_names_match", autospec=True
    )

    config_validator = ConfigValidator({"some config"})
    config_validator.validate()
    config_validator.check_default_connections.assert_called_once()
    config_validator.check_connection_names_match.assert_called_once()


# def test_check_default_connections_method(mocker):
    # class Mocked(simqle.config_loader.DefaultConnectionConfigValidator):
        # def __init__(self, config):
            # self.config = config

        # def validate(self):
            # return "default connection name"

    # mocker.patch("simqle.config_loader.DefaultConnectionConfigValidator", new=Mocked)

    # config_validator = ConfigValidator({"some": "config"})
    # config_validator.check_default_connections()

    # assert config_validator.default_connection_name == "default connection name"


def test_check_connection_names_match_method(mocker):
    class Mocked(simqle.config_loader.MatchingConnectionNamesValidator):
        def __init__(self, config):
            self.config = config

        def validate(self):
            return "default connection name"

    mocker.patch("simqle.config_loader.MatchingConnectionNamesValidator", new=Mocked)
    mocker.patch.object(Mocked, "validate", autospec=True)

    config_validator = ConfigValidator({"some": "config"})
    config_validator.check_connection_names_match()

    Mocked.validate.assert_called_once()


# --- Default Connection Validator ---


# def test_default_connection_validator_init():
    # DefaultConnectionConfigValidator(config={"some": "config"})


# def test_get_default_from_connection_type_method():
    # # normal single default
    # test_config = {"connections": [{"name": "some name", "default": True}]}
    # test_class = DefaultConnectionConfigValidator(config=test_config)

    # default_name = test_class.get_default_from_connection_type("connections")

    # assert default_name == "some name"

    # # no default connections
    # test_config = {
        # "connections": [
            # {
                # "name": "some name",
            # }
        # ]
    # }
    # test_class = DefaultConnectionConfigValidator(config=test_config)

    # default_name = test_class.get_default_from_connection_type("connections")

    # assert default_name is None

    # # multiple defaults (error)
    # test_config = {
        # "connections": [
            # {"name": "some name", "default": True},
            # {"name": "another name", "default": True},
        # ]
    # }

    # test_class = DefaultConnectionConfigValidator(config=test_config)

    # with pytest.raises(simqle.exceptions.MultipleDefaultConnectionsError):
        # default_name = test_class.get_default_from_connection_type("connections")


def test_validate_method():
    test_config = {
        "connections": [
            {
                "name": "some name",
            }
        ]
    }

    # test_class = DefaultConnectionConfigValidator(config=test_config)


def test_default_loader():
    config_with_default = {"default": "test default name"}
    test_loader = DefaultLoader(config=config_with_default)
    assert test_loader.default_connection_name == "test default name"

    config_with_default = {"something else": "some other data"}
    test_loader = DefaultLoader(config=config_with_default)
    assert test_loader.default_connection_name is None
