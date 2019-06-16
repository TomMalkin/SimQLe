"""Load Constants."""
DEV_MAP = {
    # test mode: connection heading in yaml file
    True: "test-connections",
    False: "connections",
}

# TODO: add other default locations.
DEFAULT_FILE_LOCATIONS = [
    "./.connections.yaml",
]
