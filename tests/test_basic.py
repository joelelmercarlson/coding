from .context import team
import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test case."""
    def test_true(self):
        assert True

if __name__ == '__main__':
    unittest.main()
