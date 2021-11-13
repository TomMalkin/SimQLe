"""
Define ConfigLoader and ConfigValidator.

ConfigLoader is responsible for loading a config dict that can be passed to a ConnectionManager
object from a .connections.yaml filename parameter.

ConfigValidator is responsible for checking and validating the configuration has no errors.
"""
from yaml import safe_load

from .logging import logger
from .constants import DEFAULT_FILE_LOCATIONS, MODE_MAP
from .exceptions import NoConnectionsFileError, EnvironSyncError, MultipleDefaultConnectionsError


class ConfigLoader:
    """Load the configuration with connection details from a given filename and mode."""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

        self.config_section_name = MODE_MAP.get(self.mode, "connections")

        self.base_config = self.load_config()

        self.validator = ConfigValidator(config=self.base_config)
        self.validator.validate()

        self.default_connection_name = self.validator.default_connection_name

        self.config = self.base_config.get(self.config_section_name)

    def load_config(self):
        """
        Load connections config dict from a .connections.yaml file.

        If a filename isn't given, then look for the .connections.yaml file in a list of default
        locations.

        If the filename is a dict, then load that as the config.
        """
        base_config = None

        if not self.filename:
            base_config = self.load_from_default_location()

        elif isinstance(self.filename, dict):
            base_config = self.filename
            logger.info("Configuration loaded from a given dict parameter, rather than a filename.")
        else:
            try:
                base_config = self.load_file(filename=self.filename)
            except FileNotFoundError as exception:
                raise FileNotFoundError(
                    f"Cannot find the specified connections file [{self.filename}]"
                ) from exception

            logger.info(f"Configuration loaded from file [filename={self.filename}]")

        return base_config

    def load_from_default_location(self):
        """Load a .connections.yaml file from the first valid default location."""
        config = None
        for default_filename in DEFAULT_FILE_LOCATIONS:
            try:
                config = self.load_file(default_filename)

                logger.info(
                    f"Configuration loaded from default location [location='{default_filename}']"
                )

                break

            except FileNotFoundError:
                continue

        if not config:
            raise NoConnectionsFileError(
                "No filename is specified and no files in default locations are found."
            )

        return config

    @staticmethod
    def load_file(filename):
        """Load the specified filename."""
        with open(filename, mode="r", encoding="utf8") as file:
            return safe_load(file.read())


class ConfigValidator:
    """Validate a configuration."""

    def __init__(self, config):
        self.config = config
        self.default_connection_name = None

    def validate(self):
        """Run all validators on the config."""
        self.check_default_connections()
        self.check_connection_names_match()

    def check_default_connections(self):
        """Check the validity of any default connections."""
        self.default_connection_name = DefaultConnectionConfigValidator(self.config).validate()

    def check_connection_names_match(self):
        """Check that the connection names match in all connection modes."""
        MatchingConnectionNamesValidator(self.config).validate()


class DefaultConnectionConfigValidator:
    """
    Validator that for each simqle mode, only one default connection exists.

    Stores the default connection for use later.
    """

    def __init__(self, config):
        self.config = config

    def get_default_from_connection_type(self, connection_type):
        """Find the default connection in the config."""
        number_of_defaults = 0

        for connection in self.config[connection_type]:
            if connection.get("default"):
                number_of_defaults += 1
                default_connection_name = connection.get("name")

                logger.info(f"Setting default connection [name = '{connection.get('name')}']")

        if not number_of_defaults:
            return None

        if number_of_defaults > 1:
            raise MultipleDefaultConnectionsError("More than 1 default connection was specified.")

        return default_connection_name

    def validate(self):
        """Validate that there is one default connection name and they match across types."""
        default_connection_name = self.get_default_from_connection_type("connections")

        if not default_connection_name:
            return

        logger.info(f"Setting default connection [name = '{default_connection_name}']")

        dev_default_connection_name = self.get_default_from_connection_type("dev-connections")

        if default_connection_name != dev_default_connection_name:
            raise EnvironSyncError(
                "The default connections in production and development do not match, "
                f"the production default is [{default_connection_name}] and the dev default "
                f"is [{dev_default_connection_name}]"
            )

        test_default_connection_name = self.get_default_from_connection_type("test-connections")

        if default_connection_name != test_default_connection_name:
            raise EnvironSyncError(
                "The default connections in production and development do not match, "
                f"the production default is [{default_connection_name}] and the dev default "
                f"is [{test_default_connection_name}]"
            )


class MatchingConnectionNamesValidator:  # noqa: R0903
    """Validate that the connection names in the 3 simqle modes are the same."""

    def __init__(self, config):
        self.config = config

    def validate(self):
        """Validate on this instance's config."""
        production_names = {connection["name"] for connection in self.config["connections"]}

        if self.config.get("dev-connections"):
            dev_names = {connection["name"] for connection in self.config["dev-connections"]}
            if production_names != dev_names:
                raise EnvironSyncError(
                    "The connections names in the production connections and the development"
                    "connections do not match"
                )

        if self.config.get("test-connections"):
            dev_names = {connection["name"] for connection in self.config["test-connections"]}
            if production_names != dev_names:
                raise EnvironSyncError(
                    "The connections names in the production connections and the testing"
                    "connections do not match"
                )
