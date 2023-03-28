"""Load Constants."""

from os.path import expanduser, join

MODE_MAP = {
    "production": "connections",
    "development": "dev-connections",
    "testing": "test-connections",
}

DEFAULT_FILE_LOCATIONS = [
    "./.connections.yaml",

    # the home folder on either Linux or Windows
    join(expanduser("~"), ".connections.yaml")
]

REQUIRED_FIELDS = ["name", "driver", "connection"]
