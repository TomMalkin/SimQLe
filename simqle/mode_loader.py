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

class ModeLoader:

    def __init__(self, override=None):
        self.mode = override or os.getenv("SIMQLE_MODE", "production")

