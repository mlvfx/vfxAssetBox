"""
Path display widget for use in the main interface. Generally used to display
the path of the selected item.
"""
import assetbox.ui.qthelpers as qthelpers

try:
    from PySide import QtGui
except:
    pass


class QPath(QtGui.QWidget):
    """
    Widget with a horizontal layout to store a line edit.
    """
    def __init__(self, parent=None):
        """Initialise the widget. Create the layout and child widgets."""
        super(QPath, self).__init__()

        path_layout = QtGui.QHBoxLayout(self)
        qthelpers.clean_layouts(path_layout)

        path_layout.addWidget(QtGui.QLabel('Path:'))
        self.path_line = QtGui.QLineEdit('...')
        self.path_line.setReadOnly(True)
        path_layout.addWidget(self.path_line)

        parent.addWidget(self)

    def get_text(self):
        """Return the text from the path line."""
        self.path_line.text()

    def set_text(self, text):
        """Set the text in the path widget.

        Args:
            text (str): Text to place in the pathedit.
        """
        self.path_line.setText(text)
