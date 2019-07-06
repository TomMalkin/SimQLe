"""Load Constants."""
DEV_MAP = {
    "production": "connections",
    "development": "dev-connections",
    "testing": "test-connections",
}

# TODO: add other default locations.
DEFAULT_FILE_LOCATIONS = [
    "./.connections.yaml",
]
