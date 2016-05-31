"""
Project Selector is a QComboBox to pick projects.
"""
from PySide import QtGui
from PySide import QtCore

from assetbox.base import helpers
import assetbox.ui.qthelpers as qthelpers


class QProjectCombo(QtGui.QWidget):
    """
    The primary combobox for selecting projects.
    """
    def __init__(self, parent=None, project=None):
        """
        Initialise the widget.

        Args:
            parent (QtGui.QLayout): The parent layout to add this to.
            project (str): The default project to set the index to.
        """
        super(QProjectCombo, self).__init__()

        self.default_project = project

        self.layout = QtGui.QHBoxLayout(self)
        qthelpers.clean_layouts(self.layout, margin=0)

        _label = QtGui.QLabel('Projects:')
        _label.setFixedWidth(45)
        self.layout.addWidget(_label, stretch=0)
        self._combo = QtGui.QComboBox()
        self.layout.addWidget(self._combo)

        parent.addWidget(self)

    def combobox(self):
        """Return the primary combobox."""
        return self._combo

    def populate_projects(self, projects_folder):
        """
        Add project folders into the combobox.

        Args:
            projects_folder (str): The project folders to add.
        """
        projects = helpers.get_folders(projects_folder)
        for p in projects:
            self._combo.addItem(p)

        if self.default_project in projects:
            index = self._combo.findText(self.default_project,
                                         QtCore.Qt.MatchFixedString)
            if index >= 0:
                self._combo.setCurrentIndex(index)

    def text(self):
        """Return the current text in the combobox."""
        return self._combo.currentText()
