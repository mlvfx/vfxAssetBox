"""
Asset display widget using a QListWidget for use in the main interface.
Generally used to display assets living in the selected folder.
"""
from PySide import QtCore
from PySide import QtGui

import assetbox.ui.qthelpers as qthelpers


class QAssetListWidget(QtGui.QWidget):
    """
    Widget with a horizontal layout to store a line edit.
    """
    def __init__(self, parent=None):
        """Initialise the widget. Create the layout and child widgets."""
        super(QAssetListWidget, self).__init__()

        _layout = QtGui.QVBoxLayout(self)
        qthelpers.clean_layouts(_layout)

        self.list_addons = QtGui.QWidget()
        self.list_addons_layout = QtGui.QHBoxLayout(self.list_addons)
        qthelpers.clean_layouts(self.list_addons_layout)
        _layout.addWidget(self.list_addons)

        self.list_addons_layout.addWidget(QtGui.QLabel('Assets:'))

        # Setup the search line.
        self.search_lineedit = QtGui.QLineEdit('')
        self.search_lineedit.setPlaceholderText('Search...')
        self.search_lineedit.textChanged.connect(self.__search_filter_results)
        self.list_addons_layout.addWidget(self.search_lineedit)

        # Setup the fontsize slider.
        self.horizontal_slider = QtGui.QSlider()
        self.horizontal_slider.setMinimum(4)
        self.horizontal_slider.setMaximum(18)
        self.horizontal_slider.setValue(8)
        self.horizontal_slider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_slider.valueChanged.connect(self.__adjust_list_fontsize)
        self.list_addons_layout.addWidget(self.horizontal_slider)

        # Setup the main list widget.
        self._list_widget = QtGui.QListWidget()
        self._list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self._list_widget.customContextMenuRequested.connect(self.selected_asset_rightclicked)
        # self._list_widget.itemClicked.connect(self.selected_asset)

        # Create custom path attribute.
        self._list_widget.path = ''

        _layout.addWidget(self._list_widget)
        parent.addWidget(self)

    def add_item(self, item):
        """
        Add an asset to the list widget.

        Args:
            item (assetbox.base.assets.Asset): The asset item.
        """
        family = item.font().family()
        value = self.horizontal_slider.value()
        font = QtGui.QFont(family, value)
        item.setFont(font)

        self._list_widget.addItem(item)

    def list_widget(self):
        """Return the primary list widget."""
        return self._list_widget

    def path(self):
        """Return the path attribute."""
        return self._list_widget.path

    def set_path(self, path):
        """Set the path attribute.

        Args:
            path (str): The path to show assets for.
        """
        self._list_widget.path = path

    def clear(self):
        """Clear the list widget."""
        self._list_widget.clear()

    def __search_filter_results(self, text):
        """
        Filter the assets based on the search filter.

        Args:
            text (str): The filter text.
        """
        items = []
        for index in xrange(self._list_widget.count()):
            items.append(self._list_widget.item(index))

        if not items:
            return

        for item in items:
            if text in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def __adjust_list_fontsize(self, value):
        """
        Modify the font size based on a horizontal slider.

        Args:
            value (int): Size of the font.
        """
        items = []
        for index in xrange(self._list_widget.count()):
            items.append(self._list_widget.item(index))

        if not items:
            return

        family = items[0].font().family()

        font = QtGui.QFont(family, value)
        for item in items:
            item.setFont(font)
