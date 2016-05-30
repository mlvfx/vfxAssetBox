"""
Generic file browser for use throughout the app.
"""
import os

from PySide import QtGui


class QFileBrowser(QtGui.QFileDialog):
    """
    A filebrowser widget made from a QFileDialog.
    """
    def __init__(self, parent=None, text=''):
        """Initialise the widget."""
        super(QFileBrowser, self).__init__()
        self.parent = parent
        self.text = text

    def get_folder(self):
        """Find and return a folder. Shows only directories."""
        dir_ = self.getExistingDirectory(parent=self.parent, caption=self.text)

        if not dir_:
            dir_ = os.path.abspath('..')

        return dir_
