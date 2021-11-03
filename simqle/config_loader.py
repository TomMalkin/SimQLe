"""
Define ConfigLoader and ConfigValidator.

ConfigLoader is responsible for loading a config dict that can be passed to a ConnectionManager
object from a .connections.yaml filename parameter.

ConfigValidator is responsible for checking and validating the configuration has no errors.
"""

from .logging import logger
from .constants import DEFAULT_FILE_LOCATIONS
from .exceptions import NoConnectionsFileError


class ConfigLoader:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

        self.config = self.load_config()

        self.validator = ConfigValidator(config=self.config)
        self.validator.validate()

    def load_config(self, filename, mode):
        """
        Load connections config dict from a .connections.yaml file.

        If a filename isn't given, then look for the .connections.yaml file in a list of default
        locations.

        If the filename is a dict, then load that as the config.
        """
        config = None

        if not filename:
            config = self.load_from_default_location()
            return config

        if isinstance(file_name, dict):
            config = file_name
            logger.info(
                f"Configuration loaded from a given dict parameter, rather than a filename."
            )
            return config

        try:
            config = self.load_file(filename=filename)
        except FileNotFoundError:
            raise FileNotFoundError(f"Cannot find the specified connections file [{filename}]")

        logger.info(f"Configuration loaded from file [filename={filename}]")

        return config

    def load_from_default_location(self):
        config = None
        for default_filename in DEFAULT_FILE_LOCATIONS:
            try:
                config = self.load_file(filename=default_filename)

                logger.info(
                    f"Configuration loaded from default location [location={default_filename}]"
                )

                return config

            except FileNotFoundError:
                continue

        if not config:
            raise NoConnectionsFileError(
                "No file_name is specified and no files in default locations are found."
            )

    def load_file(self, filename):
        with open(filename) as file:
            return safe_load(file.read())


class ConfigValidator:

    def __init__(self, config):
        self.config = config

        self.validate()

    def validate(self):
        self.check_default_connections()
        self.check_connection_names_match()

    def check_default_connections(self):
        pass

    def check_connection_names_match(self):
        pass

