"""
Tests to test the tests.
"""
import unittest


class TestClass(unittest.TestCase):

    def test_one(self):
        """Test One."""
        one = True
        self.assertTrue(one)

    def test_two(self):
        """Test Two."""
        two = False
        self.assertFalse(two)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
