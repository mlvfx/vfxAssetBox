"""
Breadcrumb widget for use in the main interface.
"""
try:
    from PySide import QtGui
    from PySide import QtCore
    from functools import partial
except:
    pass


class QBreadcrumb(QtGui.QWidget):
    """Primary Breadcrumb widget."""
    def __init__(self, parent=None):
        """Initialise the widget."""
        super(QBreadcrumb, self).__init__(parent)
        self.parent = parent
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(2)
        self.setVisible(False)

        # Set the palette
        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), QtGui.QColor(20, 20, 21))
        # self.setPalette(p)

        # Set the margin
        m = 2
        self.layout.setContentsMargins(m, m, m, m)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.buttons = []
        self.dividers = []

        num_of_buttons = 5
        for value in range(num_of_buttons):
            self._add_button()

    def _hide_all(self):
        """Hide all of the buttons."""
        for button in self.buttons:
            button.setVisible(False)
        for divider in self.dividers:
            divider.setVisible(False)

    def set_breadcrumb_label(self, *args):
        """Set the label of the bread crumbs."""
        self.setVisible(True)
        button_activators = [args[-1]]
        parent = args[-1].parent()
        if parent:
            button_activators.append(parent)
            while parent.parent() is not None:
                parent = parent.parent()
                button_activators.append(parent)

        if button_activators:
            button_activators.reverse()
            for idx, item in enumerate(button_activators):
                self.buttons[idx].setText(item.get_name())
                width = self.buttons[idx].fontMetrics().boundingRect(self.buttons[idx].text()).width()
                self.buttons[idx].setFixedWidth(width+15)
                self.buttons[idx].setVisible(True)
                self.dividers[idx].setVisible(True)
                self.buttons[idx].item = item
                # _partial = partial(self._select_in_tree, item)
                # self.buttons[idx].clicked.connect(_partial)

    def _select_in_tree(self, button):
        """When selecting a breadcrumb, select it in the treewidget."""
        self.parent.folder_tree.setCurrentItem(button.item)
        self.parent._populate_assets(button.item)

    def _add_button(self):
        """Add a breadcrumb button widget."""
        button = QtGui.QPushButton('..')
        button.setFlat(True)
        button.setFixedWidth(70)
        button.setVisible(False)
        _partial = partial(self._select_in_tree, button)
        button.clicked.connect(_partial)
        self.layout.addWidget(button)
        self._add_divider()
        self.buttons.append(button)

    def _add_divider(self):
        """Add a > arrow separator in the widget."""
        divider = QtGui.QLabel('>')
        divider.setFixedWidth(8)
        divider.setVisible(False)
        self.layout.addWidget(divider)
        self.dividers.append(divider)
