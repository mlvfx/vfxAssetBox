"""
Host app for modo, check if we are in modo.
"""
from assetbox.base.plugins.host import BaseHost
import sys


class HostApp(BaseHost):
    """
    The host application class, which is used to determine context.
    """
    ID = 'Modo'
    FILETYPES = ['abc']

    def get_host(self):
        """Return True if we are in Modo."""
        return 'modo' in sys.executable

    def start_QApp(self):
        """Create the QApplication."""
        pass
