"""
Assets used by the interface.
"""
from PySide import QtGui
import os
import uuid


class Location(QtGui.QTreeWidgetItem):
    """Location widget is used in the folder structure treewidget."""

    id_ = uuid.uuid4()

    def __init__(self, parent, name, path):
        """Initialise the class."""
        super(Location, self).__init__(parent)

        self.setText(0, name)
        self._path = path.replace("\\", "/")

    def get_name(self):
        """Return the name."""
        return self.text(0)

    def get_path(self):
        """Return the path."""
        return self._path

    def is_file(self):
        """Returns True if this is a file."""
        return os.path.isfile(self.get_path())

    def is_dir(self):
        """Returns True if this is a directory."""
        return not os.path.isfile(self.get_path())


class Asset(QtGui.QListWidgetItem):
    """Asset is the widget used to represent widgets."""

    filetype = None
    actions = []

    def __init__(self, parent, name, path):
        """Initialise the class."""
        super(Asset, self).__init__(parent)

        self.setText(name)
        self._path = path.replace("\\", "/")

        name, ext = os.path.splitext(self._path)
        self.filetype = ext.replace('.', '')

    def get_name(self):
        """Return the name."""
        return self.text()

    def get_path(self):
        """Return the path."""
        return self._path

    def get_actions(self):
        """Returns True if this is a file."""
        return self.actions

    def add_actions(self, actions):
        """Returns True if this is a directory."""
        self.actions = actions
