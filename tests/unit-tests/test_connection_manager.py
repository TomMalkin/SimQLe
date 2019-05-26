
import unittest

from simqle.connection_manager import ConnectionManager  

TEST_FILE = 'tests/integration-tests/mysql-tests/.connections.yaml'

class TestConnectionManager(unittest.TestCase):

    def test(self):
        connection_mananger = ConnectionManager(TEST_FILE)

if __name__ == '__main__':
    unittest.main()
