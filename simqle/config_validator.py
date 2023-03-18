"""Provide a validator for the given configuration."""

from jsonschema import validate

CONNECTIONS_FILE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://json-schema.org/draft-07/schema#",
    "definitions": {
        "connection": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "driver": {"type": "string"},
                "connection": {"type": "string"},
                "url_escape": {"type": "boolean"},
            },
            "required": ["name", "driver", "connection"],
            "additionalProperties": False,
        }
    },
    "type": "object",
    "properties": {
        "connections": {"type": "array", "items": {"#ref": "#/definitions/connection"}},
        "dev-connections": {"type": "array", "items": {"#ref": "#/definitions/connection"}},
        "test-connections": {"type": "array", "items": {"#ref": "#/definitions/connection"}},
        "default": {"type": "string"},
    },
    "additionalProperties": False,
    "AnyOf": [
        {"required": ["connections"]},
        {"required": ["dev-connections"]},
        {"required": ["test-connections"]},
    ],
}


def validate_configuration(configuration):
    """Validate a loaded configuration file against a schema."""
    return validate(instance=configuration, schema=CONNECTIONS_FILE_SCHEMA)
