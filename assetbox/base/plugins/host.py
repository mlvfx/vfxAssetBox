"""
Base host class to give skeleton structure for a plugin host.
"""
import sys
from PySide import QtGui


class BaseHost(object):
    """
    The host application class, which is used to determine context.
    """
    id_ = 'python'
    inhost = False
    filetypes = ['abc']

    def __init__(self):
        self.inhost = self.get_host()

    def get_host(self):
        """Return True if we are in a python interpreter."""
        return 'python' in sys.executable

    def start_QApp(self):
        """Create the QApplication."""
        try:
            app = QtGui.QApplication(sys.argv)
            # app = QtGui.QApplication(["python"])
        except RuntimeError:
            app = QtGui.QApplication.instance()

        sys.exit(app.exec_())
