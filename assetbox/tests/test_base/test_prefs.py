"""
Test the prefs class.
"""
import unittest


class TestPrefsHelperClass(unittest.TestCase):

    def test_create_config(self):
        """Create and read a config."""
        import assetbox.base.prefs

        preferences = assetbox.base.prefs.PreferenceHelper()
        preferences.config.set('project', 'test', 'result')

        self.assertEquals(preferences.config.get('project', 'test'), 'result')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
