"""
Widget that stores action buttons from the host application.
"""
from PySide import QtGui

import assetbox.ui.qthelpers as qthelpers


class QActionButtons(QtGui.QWidget):
    """
    QWidget with a hbox layout for action buttons.
    """
    def __init__(self, parent=None):
        """Initialise the widget. Create the layout."""
        super(QActionButtons, self).__init__()

        self.layout = QtGui.QHBoxLayout(self)
        qthelpers.clean_layouts(self.layout)
        parent.addWidget(self)

    def add_button(self, name, action):
        """
        Add a QPushButton object to the layout.

        Args:
            name (str): Name/label to add to the button.
            action (object): function call to add to button.
        """
        _button = QtGui.QPushButton(name)
        _button.clicked.connect(action)

        self.layout.addWidget(_button)
