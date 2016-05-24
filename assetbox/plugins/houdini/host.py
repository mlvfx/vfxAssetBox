"""
Host app for Houdini, check if we are in Sidefx Houdini.
"""
from assetbox.base.plugins.host import BaseHost
import sys


class HostApp(BaseHost):
    """
    The host application class, which is used to determine context.
    """
    ID = 'Houdini'
    FILETYPES = ['abc']

    def get_host(self):
        """Return True if we are in Houdini."""
        return 'houdini' in sys.executable
