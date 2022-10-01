"""
Define ConfigLoader and ConfigValidator.

ConfigLoader is responsible for loading a config dict that can be passed to a ConnectionManager
object from a .connections.yaml filename parameter.

ConfigValidator is responsible for checking and validating the configuration has no errors.
"""

from yaml import safe_load

from .constants import DEFAULT_FILE_LOCATIONS, MODE_MAP, REQUIRED_FIELDS
from .exceptions import (
    EnvironSyncError,
    MissingFieldError,
    NoConnectionsFileError,
    UnknownSourceTypeError,
)
from .logging import logger


class ConfigLoader:
    """Load the configuration with connection details from a given src and mode."""

    def __init__(self, src, mode):
        """
        Initialise the ConfigLoader from a src and mode.

        The section of the .connections.yaml file that we will load from is based on the MODE_MAP.

        The config is also passed to a validator, to make sure the config has the required fields.
        """
        self.src = src
        self.mode = mode

        self.section_name = self.get_section_name(self.mode)

        self.full_config = self.load_config()

        self.validate(self.full_config)

        self._config = self.full_config.get(self.section_name)

    @property
    def config(self):
        """Get property config."""
        return self._config

    @staticmethod
    def get_section_name(mode):
        """Return the section of the config to use for a given mode."""
        return MODE_MAP.get(mode, "connections")

    @staticmethod
    def validate(full_config):
        """Validate the configuration."""
        ConfigValidator(config=full_config).validate()

    def load_config(self):
        """
        Load connections config dict from a src.

        If a filename isn't given, then look for the .connections.yaml file in a list of default
        locations.

        If the filename is a dict, then load that as the config.
        """
        base_config = None

        if self.src is None:
            base_config = self.load_from_default_location()

        elif isinstance(self.src, dict):
            base_config = self.src
            logger.info("Configuration loaded from a given dict parameter, rather than a filename.")

        elif isinstance(self.src, str):
            try:
                base_config = self.load_file(filename=self.src)
            except FileNotFoundError as exception:
                raise FileNotFoundError(
                    f"Cannot find the specified connections file [{self.src}]"
                ) from exception

            logger.info(f"Configuration loaded from file [filename={self.src}]")

        else:
            raise UnknownSourceTypeError(
                f"Unknown type for supplied src parameter: {type(self.src)}"
            )

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
        """Initialise a ConfigValidator."""
        self.config = config

    def validate(self):
        """Run all validators on the config."""
        self.check_connection_names_match()
        self.check_each_connection_has_required_fields()

    def check_connection_names_match(self):
        """Check that the connection names match in all connection modes."""
        validate_matching_connection_names(self.config)

    def check_each_connection_has_required_fields(self):
        """
        Check that each connection in the yaml file has the 3 required fields.

        These fields are:
         - name
         - driver
         - connection
        """
        validate_connection_required_fields(self.config)


def load_default_connection_name(config):
    """Get the default connection name."""
    if not config.get("default"):
        logger.warning(
            "Default Connection Name not set in connection file. con_name must "
            "always be specified"
        )
        return None
    return config.get("default")


# class DefaultConnectionConfigValidator:
# """
# Validator that for each simqle mode, only one default connection exists.

# Stores the default connection for use later.
# """

# def __init__(self, config):
# self.config = config

# def get_default_from_connection_type(self, connection_type):
# """Find the default connection in the config."""
# number_of_defaults = 0

# for connection in self.config[connection_type]:
# if connection.get("default"):
# number_of_defaults += 1
# default_connection_name = connection.get("name")

# logger.info(f"Setting default connection [name = '{connection.get('name')}']")

# if not number_of_defaults:
# return None

# if number_of_defaults > 1:
# raise MultipleDefaultConnectionsError("More than 1 default connection was specified.")

# return default_connection_name

# def validate(self):
# """Validate that there is one default connection name and they match across types."""
# default_connection_name = self.get_default_from_connection_type("connections")

# if not default_connection_name:
# return

# logger.info(f"Setting default connection [name = '{default_connection_name}']")

# dev_default_connection_name = self.get_default_from_connection_type("dev-connections")

# if default_connection_name != dev_default_connection_name:
# raise EnvironSyncError(
# "The default connections in production and development do not match, "
# f"the production default is [{default_connection_name}] and the dev default "
# f"is [{dev_default_connection_name}]"
# )

# test_default_connection_name = self.get_default_from_connection_type("test-connections")

# if default_connection_name != test_default_connection_name:
# raise EnvironSyncError(
# "The default connections in production and development do not match, "
# f"the production default is [{default_connection_name}] and the dev default "
# f"is [{test_default_connection_name}]"
# )


def validate_matching_connection_names(config):
    """Validate that the connection names in the 3 simqle modes are the same."""
    production_names = {connection["name"] for connection in config["connections"]}

    if config.get("dev-connections"):
        dev_names = {connection["name"] for connection in config["dev-connections"]}
        if production_names != dev_names:
            raise EnvironSyncError(
                "The connections names in the production connections and the development"
                "connections do not match"
            )

    if config.get("test-connections"):
        dev_names = {connection["name"] for connection in config["test-connections"]}
        if production_names != dev_names:
            raise EnvironSyncError(
                "The connections names in the production connections and the testing"
                "connections do not match"
            )


# class MatchingConnectionNamesValidator:  # noqa: R0903
# """Validate that the connection names in the 3 simqle modes are the same."""

# def __init__(self, config):
# self.config = config

# def validate(self):
# """Validate on this instance's config."""
# production_names = {connection["name"] for connection in self.config["connections"]}

# if self.config.get("dev-connections"):
# dev_names = {connection["name"] for connection in self.config["dev-connections"]}
# if production_names != dev_names:
# raise EnvironSyncError(
# "The connections names in the production connections and the development"
# "connections do not match"
# )

# if self.config.get("test-connections"):
# dev_names = {connection["name"] for connection in self.config["test-connections"]}
# if production_names != dev_names:
# raise EnvironSyncError(
# "The connections names in the production connections and the testing"
# "connections do not match"
# )


def validate_connection_required_fields(config):
    """Validate that the connection names in the 3 simqle modes are the same."""
    for connection_mode in ["connections", "dev-connections", "test-connections"]:
        for connection in config.get(connection_mode, []):
            for required_field in REQUIRED_FIELDS:
                if required_field not in connection.keys():
                    msg = (
                        "Missing field in connection [missing"
                        f"field={required_field}, connection"
                        f"mode={connection_mode}]"
                    )
                    raise MissingFieldError(msg)

    production_names = {connection["name"] for connection in config["connections"]}

    if config.get("dev-connections"):
        dev_names = {connection["name"] for connection in config["dev-connections"]}
        if production_names != dev_names:
            raise EnvironSyncError(
                "The connections names in the production connections and the development"
                "connections do not match"
            )

    if config.get("test-connections"):
        dev_names = {connection["name"] for connection in config["test-connections"]}
        if production_names != dev_names:
            raise EnvironSyncError(
                "The connections names in the production connections and the testing"
                "connections do not match"
            )
