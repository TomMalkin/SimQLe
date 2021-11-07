"""
Define the ModeLoader class.

ModeLoader is responsible for loading the mode that simqle should run in:
 - production
 - development
 - testing

Loading the connections from the config based on the above mode:
 - production: connections
 - development: dev-connections
 - testing: test-connections
"""

import os


def mode_loader(override=None):
    """Return the simqle mode from the SIMQLE_MODE env var and an optional override."""
    return override or os.getenv("SIMQLE_MODE", "production")
