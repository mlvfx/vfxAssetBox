"""
Host app for nuke, check if we are in nuke.
"""
from assetbox.base.plugins.host import BaseHost
import sys


class HostApp(BaseHost):
    """
    The host application class, which is used to determine context.
    """
    ID = 'Nuke'
    filetypes = ['abc', 'exr']

    def get_host(self):
        """Return True if we are in Nuke."""
        return 'Nuke' in sys.executable

    def start_QApp(self):
        """Create the QApplication."""
        pass
