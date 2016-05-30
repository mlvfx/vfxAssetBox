"""
Host app for maya, check if we are in maya.
"""
from assetbox.base.plugins.host import BaseHost
import sys


class HostApp(BaseHost):
    """
    The host application class, which is used to determine context.
    """
    id_ = 'Maya'
    filetypes = ['abc', 'png', 'tiff']

    def get_host(self):
        """Return True if we are in Maya."""
        return 'Maya' in sys.executable

    def start_QApp(self):
        """Create the QApplication."""
        pass
