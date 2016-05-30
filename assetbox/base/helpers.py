"""Generic helper classes and functions."""
import fnmatch
import os


class FolderHelper(object):
    """Methods to check folder attributes."""

    def is_hidden(self, filepath):
        """
        Check if a file is hidden in the os.

        Args:
            filepath (str): path to a file.

        Returns:
            bool: True if a file is hidden.
        """
        name = os.path.basename(os.path.abspath(filepath))
        return name.startswith('.') or self.has_hidden_attribute(filepath)

    def has_hidden_attribute(self, filepath):
        """
        Check if a file has a hidden attribute.

        Args:
            filepath (str): path to a file.

        Returns:
            bool: True if a file has a hidden attribute.
        """
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
            assert attrs != -1
            result = bool(attrs & 2)
        except (AttributeError, AssertionError):
            result = False
        return result


def get_files(folder, pattern='*.abc'):
    """
    Passing a folder and a pattern match, return all files.

    Args:
        folder (str): path to a folder.
        pattern (str): a pattern to match, usually a file extension.

    Returns:
        list: all matching files in the folder.
    """
    matches = []

    if os.path.isdir(folder):
        for root, dirnames, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename).replace("\\", "/"))

        return matches
    else:
        return matches


def join_path(*args):
    """
    Join paths fixing slashes for windows.

    Args:
        args (list[str]): the folder/file path to join.

    Return:
        str: the resolved path.
    """
    return os.path.join(*args).replace("\\", "/")


def search_id(search_dict, uid):
    """
    | Search in a dictionary if the dict values ID attribute matches
    | the passed id.

    Args:
        search_dict (dict): the dict to search.
        uid (str): unique id to query.

    Returns:
        str: return the found key from the dict.
    """
    for key, value in search_dict.items():
        for v in value:
            if uid in v.id_:
                return key
