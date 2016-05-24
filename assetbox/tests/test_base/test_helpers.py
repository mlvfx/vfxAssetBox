"""
Test the helper class.
"""
import unittest
import os


class TestHelperClass(unittest.TestCase):

    def test_folderhelper_ishidden(self):
        """File is hidden in the os."""
        import assetbox.base.helpers

        txt_file = os.path.abspath('../content/.test_file.txt')
        fh = assetbox.base.helpers.FolderHelper()

        self.assertTrue(fh.is_hidden(txt_file))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
