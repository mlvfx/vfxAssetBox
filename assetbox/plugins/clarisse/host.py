"""
Host app for Clarisse, check if we are in Isotropix Clarisse.
"""
from assetbox.base.plugins.host import BaseHost
import sys
from PySide import QtGui


class HostApp(BaseHost):
    """
    The host application class, which is used to determine context.
    """
    ID = 'Clarisse'
    FILETYPES = ['abc', 'png', 'tiff', 'vdb']

    def get_host(self):
        """Return True if we are in Clarisse."""
        return 'Clarisse' in sys.executable

    def start_QApp(self):
        """Create the QApplication."""
        import pyqt_clarisse

        try:
            app = QtGui.QApplication(["Clarisse"])
        except:
            app = QtGui.QApplication.instance()

        pyqt_clarisse.exec_(app)
