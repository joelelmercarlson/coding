from .context import team
import unittest

class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""
    def test_true(self):
        assert True

if __name__ == '__main__':
    unittest.main()
