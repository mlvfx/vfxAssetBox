"""
Folder Tree Widget for displaying the folder structure.
"""
from PySide import QtGui


class QFolderTree(QtGui.QTreeWidget):
    """
    The primary tree widget for displaying the folder structure.
    """
    def __init__(self, parent=None):
        """Initialise the widget."""
        super(QFolderTree, self).__init__()

        # tree_browser_widget.itemClicked.connect(self._populate_assets)
        self.setHeaderHidden(True)
        parent.addWidget(self)
